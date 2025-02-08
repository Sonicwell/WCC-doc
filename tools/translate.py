import polib
from googletrans import Translator

# 加载 .po 文件
po_file = '/usr/src/WCC-doc/docs/source/locales/en/LC_MESSAGES/root手册.po'
po = polib.pofile(po_file)

# 初始化翻译工具
translator = Translator()

# 批量翻译
for entry in po:
    if not entry.translated():  # 如果没有翻译
        entry.msgstr = translator.translate(entry.msgid, src='zh-cn', dest='en').text  # 翻译成日语

# 保存翻译后的 .po 文件
po.save('/usr/src/WCC-doc/docs/source/locales/en/LC_MESSAGES/root手册_translated.po')
