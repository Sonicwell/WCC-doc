## 1 关于密钥对

client添加/编辑时，增加一个选项卡，EAPI, 设置如下：

- IP白名单，如果设置，则只允许白名单请求接口.包括access_token获取。

- 如果客户未进行设置证书：
```
1.允许客户上传一个公钥文件。

2.也可以点击自动生成密钥对按钮进行生成。

3.设置一个公钥描述
```

- 如果客户已设置证书：
```
1.展示公钥匙串....省略过长 和 描述。

2.允许重新上传公钥或重新生成密钥对。之前的作废。
```

- 服务器只保留公钥，私钥提醒客户自行保存好。

- 如果客户自行上传公钥, 告知标准: RSA AES-256 2048位 pem格式, 示例
```
openssl genpkey -algorithm RSA -out private_key.pem -aes256 -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in private_key.pem -out public_key.pem

#客户应把public_key.pem内容粘贴给我们

-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIBTAYJKoZIhvcNAQcDoIIBVzCCARwCAQExDjAMBgNVBAkMBXJlY2VydDAf
...
-----END ENCRYPTED PRIVATE KEY-----
```

- 由我们生成密钥对及签名验证示例代码
```
const crypto = require('crypto');

// 生成公私密钥对
const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', {
  modulusLength: 2048, // 密钥长度
  publicKeyEncoding: {
    type: 'spki', // 公钥编码格式
    format: 'pem', // 公钥格式
  },
  privateKeyEncoding: {
    type: 'pkcs8', // 私钥编码格式
    format: 'pem', // 私钥格式
  },
});

// 客户端用私钥签名数据
const data = "This is a string to be signed";
const sign = crypto.createSign('SHA256');
sign.update(data);
const signature = sign.sign(privateKey, 'base64');
console.log('Signature:', signature);

// 服务端用公钥验证签名
const verify = crypto.createVerify('SHA256');
verify.update(data);
const isVerified = verify.verify(publicKey, signature, 'base64');
console.log('Signature Verified:', isVerified); // 输出 true 表示验证成功
```

## 2 JWT构造规则

JWT 由三个部分组成：标头、声明集和签名。标头和声明集是 JSON 对象。这些 JSON 对象会序列化为 UTF-8 字节，然后使用 Base64url 编码进行编码。这种编码可抵御因重复编码操作而导致的编码更改。标头、声明集和签名会使用句点 (.) 字符串联在一起。

- JWT 的构成如下：
```
{Base64url encoded header}.{Base64url encoded claim set}.{Base64url encoded signature}
```

- 签名的字符串基础如下所示：
```
{Base64url encoded header}.{Base64url encoded claim set}
```

- 构成 JWT 标头, 服务依赖于 RSA SHA-256 算法和 JWT 令牌格式。因此，标头的 JSON 表示法如下所示：
```
{"alg":"RS256","typ":"JWT"}
```

- 构成 JWT 声明集, 
```
{
  "realm": "client realm",
  "exp": 1740127171, //到期时间，以 1970 年 1 月 1 日 00:00:00 UTC 以来的秒数指定。此值的有效期不得超过签发时间后的 1 小时。
  "iat": 1740123571 //签发时间，以 1970 年 1 月 1 日 00:00:00 UTC 以来的秒数指定。服务端允许±5秒偏移。
}
```

- 使用私钥通过 SHA256withRSA（也称为 RSASSA-PKCS1-V1_5-SIGN，使用 SHA-256 哈希函数）对输入内容的 UTF-8 表示法进行签名：
```
const data = {Base64url encoded header}.{Base64url encoded claim set};
const sign = crypto.createSign('SHA256');
sign.update(data);
const signature = sign.sign(privateKey, 'base64');
```

- 最终拼接出JWT
```
{Base64url encoded header}.{Base64url encoded claim set}.{Base64url encoded signature}
```

## 3.1 客户端换取access_token

- 请求速率限制: 每小时5次, 429 Too Many Requests.

- access_token时效性1小时, 以最后一次请求为准。

- 请求示例：
```
curl -d 'type=JWT&realm=clientRealm&token=原sapi验证串&assertion=header.claim.signature' 'https://your.wcc.domain/eapi/token'

{
  "access_token": "1/8xbJqaOZXSUZbHLl5EOtu1pxz3fmmetKx9W8CV4t79M",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

## 3.2 服务端受理JWT

- 1.请求速率检查(rate-limit-redis): 每小时3次, 429 Too Many Requests.

- 2.重复请求检查: redis分布式锁, md5(url path + 参数正序)
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

// 构建 JSON 输入示例
const jsonData = {
  "url_path": "/eapi/token",
  "type": "JWT",
  "realm": "clientRealm",
  "token": "原sapi验证串",
  "assertion": "header.claim.signature"
};

// 获取排序后的 MD5
const md5Hash = getSortedMD5(jsonData);
const lockres = await myRedis.set('LOCK:EAPI:md5Hash', `${config.serverKey}-${process.pid}-${Date.now()}`, 'NX', 'EX', 5);
if (lockres !== 'OK') {
  return res.status(409).send({error: "Duplicate request", message: "This request has already been processed"});
}

// 抢到锁，开始处理业务
```

- 3.一致性检查realm=clientRealm&token=原sapi验证串，得到公钥

- 4.如果client有IP白名单，需要验证是否符合

- 5.验证JWT claim中时间戳:
```
iat, 与我们服务器当前时间戳±5秒偏移。

exp > iat, 但是不能超出3600，超出按3600计算。
```

- 6.服务端用公钥验证JWT签名
```
const verify = crypto.createVerify('SHA256');
verify.update(header.claim);
const isVerified = verify.verify(publicKey, signature, 'base64');
console.log('Signature Verified:', isVerified); // 输出 true 表示验证成功
```

- 7.生成access_token
```
const token_string = crypto.createHash('sha256')
  .update(header.claim.signature + Date.now() + config.serverKey + process.pid)
  .digest('base64');

await myRedis.set('EAPI:TOKEN:client_realm:token_string', `${config.serverKey}-${process.pid}-${Date.now()}`, 'EX', 3600);

# 3600以客户实际差值为准，即exp-iat
```

- 8.输出
```
{
  "access_token": "1/8xbJqaOZXSUZbHLl5EOtu1pxz3fmmetKx9W8CV4t79M",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

## 4.1 客户端使用access_token进行EAPI请求

- curl 示例

您可以使用 curl 命令行应用测试这些命令。下面是一个使用 HTTP 标头选项（首选）的示例：
```
curl -H "Authorization: Bearer client_realm:access_token" https://your.wcc.domain/eapi/xxxx
```

或者，您也可以使用查询字符串参数选项：
```
curl https://your.wcc.domain/eapi/files?access_token=client_realm:access_token
```

- 访问令牌的过期时间:

WCC OAuth 2.0 授权服务器签发的访问令牌会在 expires_in 值提供的有效期过后过期。在访问令牌过期后，应用应生成另一个 JWT，对其进行签名，然后请求另一个访问令牌。


## 4.2 服务端EAPI access_token校验

- 1.请求中必须有access_token携带。

- 2.redis EAPI:TOKEN:client_realm:token_string存在。

- 3.重复请求检查: redis分布式锁, md5(url path + 参数正序),参照3.2介绍。

- 4.获取client参数，如ip白名单、api限制。

- 5.验证ip白名单。

- 6.请求速率检查(rate-limit-redis): 按client API限制中的配置进行检查, 429 Too Many Requests。

- 7.接口处理。

- 8.返回结果。

