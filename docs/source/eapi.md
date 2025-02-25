EAPI鉴权机制开发说明
===============================

OAuth 2.0 和 JWT（JSON Web Token） 的结合是目前最常用的授权和认证方案之一，广泛应用于分布式系统、API接口和微服务架构中。这两者的组合可以提供安全、无状态、可扩展的身份验证与授权机制。

## 1 关于密钥对

client添加/编辑时，增加一个选项卡，EAPI, 设置如下：

- **IP白名单**，如果设置，则只允许白名单请求接口.包括access_token获取时的接口，需要检查是否符合该client白名单。

- **如果客户未设置证书**：
```
1.显示生成密钥对按钮。

2.生成后需进行结果提示。若密钥对生成成功，需告知服务器不会存储私钥，请自行保管，丢失后只能重置。提示界面上提供私钥下载按钮。
```

- **如果客户已设置证书**：
```
1.展示证书公钥匙串内容。

2.显示重置密钥对按钮。

3.重置后需进行结果提示。若密钥对重置成功，需告知服务器不会存储私钥，请自行保管，丢失后只能重置。提示界面上提供私钥下载按钮。
```

- **密钥标准**: RSA AES-256 2048位 pem格式, openssl生成示例
```
openssl genpkey -algorithm RSA -out private_key.pem -aes256 -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in private_key.pem -out public_key.pem

#公钥public_key.pem内容片段示例

-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIBTAYJKoZIhvcNAQcDoIIBVzCCARwCAQExDjAMBgNVBAkMBXJlY2VydDAf
...
-----END ENCRYPTED PRIVATE KEY-----
```

- **我们服务器使用NodeJS生成密钥对及签名验证的示例代码**：
```
const crypto = require('crypto');

#生成公私密钥对
const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', {
  modulusLength: 2048,
  publicKeyEncoding: {
    type: 'spki',
    format: 'pem',
  },
  privateKeyEncoding: {
    type: 'pkcs8',
    format: 'pem',
  },
});

#客户端用私钥签名数据
const data = "This is a string to be signed";
const sign = crypto.createSign('SHA256');
sign.update(data);
const signature = sign.sign(privateKey, 'base64');
console.log('Signature:', signature);

#服务端用公钥验证签名
const verify = crypto.createVerify('SHA256');
verify.update(data);
const isVerified = verify.verify(publicKey, signature, 'base64');
console.log('Signature Verified:', isVerified); // 输出 true 表示验证成功
```

## 2 JWT的构造规则

JWT由三个部分组成：标头、负载和签名。标头和负载是 JSON 对象。这些 JSON 对象会序列化为 UTF-8 字节，然后使用 Base64url 编码进行编码。这种编码可抵御因重复编码操作而导致的编码更改。标头、负载和签名会使用句点 (.) 字符串联在一起。

- **JWT的构成如下**：
```
{Base64url encoded header}.{Base64url encoded payload}.{Base64url encoded signature}
```

- **签名的字符串基础如下所示**：
```
{Base64url encoded header}.{Base64url encoded payload}
```

- **构成JWT标头(header)**, 服务依赖于 RSA SHA-256 算法和 JWT 令牌格式。因此，标头的 JSON 表示法如下所示：
```
{"alg":"RS256","typ":"JWT"}
```

- **构成JWT负载(payload)**, 
```
{
  "realm": "client realm",
  "exp": 1740127171, //到期时间，以 1970 年 1 月 1 日 00:00:00 UTC 以来的秒数指定。此值的有效期不得超过签发时间后的 1 小时。
  "iat": 1740123571 //签发时间，以 1970 年 1 月 1 日 00:00:00 UTC 以来的秒数指定。服务端允许±5秒偏移。
}
```

- **使用私钥**通过 SHA256withRSA（也称为 RSASSA-PKCS1-V1_5-SIGN，使用 SHA-256 哈希函数）对输入内容的 UTF-8 表示法**进行签名**：
```
const data = {Base64url encoded header}.{Base64url encoded payload};
const sign = crypto.createSign('SHA256');
sign.update(data);
const signature = sign.sign(privateKey, 'base64');
```

- **最终拼接出JWT**
```
{Base64url encoded header}.{Base64url encoded payload}.{Base64url encoded signature}
```

## 3.1 客户端如何使用JWT换取access_token?

- **请求速率限制**: 5次/每小时, 超出提示 429 Too Many Requests.

- access_token**时效性1小时**, 以最后一次请求为准。

- **请求示例**：
```
curl -d 'type=JWT&realm=clientRealm&token=原sapi验证串&assertion=header.payload.signature' 'https://your.wcc.domain/eapi/token'

{
  "access_token": "1/8xbJqaOZXSUZbHLl5EOtu1pxz3fmmetKx9W8CV4t79M",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

## 3.2 服务端受理JWT，通过校验后，生成access_token

- **1.路由地址**：/eapi/token, POST请求。参数说明：
  ```
  type: JWT, 固定。
  realm: client realm。
  token: client sapi验证串。
  assertion: JWT构造内容。
  ```

- **2.请求速率检查**(rate-limit-redis): 5次/每小时, 超出提示 429 Too Many Requests。这是access_token接口的固有限制，适用于所有client。
  
- **3.重复请求检查**: redis分布式锁, md5(url path + 参数正序)，每5秒不得重复。
```
const crypto = require('crypto');

function getSortedMD5(jsonData) {  
  const sortedObj = Object.keys(jsonData)
    .sort()
    .reduce((acc, key) => {
      acc[key] = jsonData[key];
      return acc;
    }, {});
  const sortedJsonString = JSON.stringify(sortedObj);
  return crypto.createHash('md5').update(sortedJsonString).digest('hex');
}

#构建 JSON 输入示例
const jsonData = {
  "url_path": "/eapi/token",
  "type": "JWT",
  "realm": "clientRealm",
  "token": "原sapi验证串",
  "assertion": "header.payload.signature"
};

#获取排序后的 MD5
const md5Hash = getSortedMD5(jsonData);
const lockres = await myRedis.set('LOCK:EAPI:md5Hash', `${config.serverKey}-${process.pid}-${Date.now()}`, 'NX', 'EX', 5);
if (lockres !== 'OK') {
  return res.status(409).send({error: "Duplicate request", message: "This request has already been processed"});
}

#抢到锁，开始处理业务
```

- **4.一致性检查**通过，得到client公钥、IP白名单信息:
  ```
  参数realm和参数token需一致。
  
  参数realm和参数assertion中payload配置的realm一致。
  ```

- **5.如果client配置了IP白名单**，需要验证请求源IP是否符合。

- **6.验证JWT payload中时间戳**:
```
iat, 与我们服务器当前时间戳±5秒偏移。

exp 需要大于 iat, 但是不能超出3600，若超出则按3600计算，即最多允许1小时有效。
```

- **7.服务端用公钥publicKey验证assertion参数提供的JWT签名**
```
const verify = crypto.createVerify('SHA256');
verify.update(JWT.header + '.' + JWT.payload);
const isVerified = verify.verify(publicKey, JWT.signature, 'base64');
console.log('Signature Verified:', isVerified); // 输出 true 表示验证成功
```

- **8.生成access_token**
```
#token_string, Base64 编码会将 SHA-256 的 64 字符长十六进制字符串转换为 44 个字符长的 Base64 字符串。
const token_string = crypto.createHash('sha256')
  .update(header.payload.signature + Date.now() + config.serverKey + process.pid)
  .digest('base64');

#3600以客户实际差值为准，即JWT.payload.exp - JWT.payload.iat
await myRedis.set('EAPI:TOKEN:client_realm:token_string', `${config.serverKey}-${process.pid}-${Date.now()}`, 'EX', 3600);
```

- **9.输出结果**
```
{
  "access_token": "1/8xbJqaOZXSUZbHLl5EOtu1pxz3fmmetKx9W8CV4t79M",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

- **10.响应结果说明**
```
#TODO: 待补充
```

## 4.1 客户端如何使用access_token进行EAPI接口请求？

- **curl示例**

您可以使用 curl 命令行应用测试这些命令。下面是一个使用 HTTP 标头选项（首选）的示例：
```
curl -H "Authorization: Bearer client_realm:access_token" https://your.wcc.domain/eapi/xxxx
```

或者，您也可以使用查询字符串参数选项：
```
curl https://your.wcc.domain/eapi/files?token=client_realm:access_token
```

- **访问令牌的过期时间**:

WCC OAuth 2.0 授权服务器签发的访问令牌会在 expires_in 值提供的有效期过后过期。在访问令牌过期后，应用应生成另一个JWT，对其进行签名，然后请求另一个访问令牌。


## 4.2 服务端如何对EAPI access_token进行校验？

- 1.请求中必须有access_token携带。

- 2.redis keys中应存在`EAPI:TOKEN:client_realm:token_string`。

- 3.重复请求检查: redis分布式锁, md5(url path + 参数正序),参照3.2中关于“重复请求检查”介绍。

- 4.获取client参数，如ip白名单、api限制。

- 5.验证ip白名单。

- 6.请求速率检查(rate-limit-redis): 按client API限制中的配置进行检查, 超出提示 429 Too Many Requests。

- 7.接口业务处理。

- 8.返回结果。

- 9.响应结果说明
```
#TODO: 待补充
```

## 5 sapi与eapi的共用与管控

- 1.sapi路由关于token的验证，应改造为前置，不应参混在接口业务函数中。
  
- 2.sapi和eapi都是前置鉴权，通过后进行路由匹配。
  
- 3.sapi与eapi只是两套路由表述，均共同指向现有的接口函数中。
  
- 4.sapi和eapi可在系统中设置接口服务开关，前置检查，控制服务是否启用，未启用时，一律响应404。

