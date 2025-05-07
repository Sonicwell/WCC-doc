import polib
import requests
import re

# Google 翻译
def translate_text(text, source_lang="zh-CN", target_lang="eng"):
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": source_lang,  # 源语言自动检测 auto
        "tl": target_lang,  # 目标语言
        "dt": "t",
        "q": text,
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            result = response.json()
            return result[0][0][0]  # 解析返回的翻译文本
    except Exception as e:
        print(f"翻译失败: {text}，错误: {e}")

    return ""  # 失败时返回空字符串，保持未翻译状态

# 正则匹配 <img> 标签
img_pattern = re.compile(r'<img\s+[^>]*src=[\'"][^\'"]+[\'"][^>]*>', re.IGNORECASE)

# Markdown 格式图片 ![alt text](_static/images/root/media/image1.png)
markdown_img_pattern = re.compile(r'!\[[^\]]*\]\([^\)]+\)', re.IGNORECASE)

# 读取 PO 文件
po = polib.pofile("/usr/src/WCC-doc/docs/source/locales/en/LC_MESSAGES/client.po")

# 遍历所有条目，翻译未翻译的部分
for entry in po:
    if not entry.translated():  # 只处理未翻译的条目
        if img_pattern.search(entry.msgid) or markdown_img_pattern.search(entry.msgid):  # 如果是图片，跳过翻译
            entry.msgstr = ""  # 保持为空
            #TODO: 扫描图片语言目录进行替换
            print(f"跳过图片条目: {entry.msgid}")
        else:
            translated_text = translate_text(entry.msgid)
            if translated_text:  # 只有成功翻译才填充
                entry.msgstr = translated_text
                print(f"翻译: {entry.msgid} -> {translated_text}")
            else:
                entry.msgstr = ""  # 保持为空
                print(f"翻译失败, msgstr保持为空: {entry.msgid}")



# 保存回 PO 文件
po.save("/usr/src/WCC-doc/tools/client_translated.po")
print("翻译完成，已保存到 /usr/src/WCC-doc/tools/client_translated.po")
