## po文件更新

```
cd docs/source

sphinx-build -b gettext . _build/gettext

sphinx-intl update -p _build/gettext -l en -l ja -l zh_CN
```

## 使用脚本进行自动翻译

```
cd tools

export http_proxy=http://192.168.1.91:7890

export https_proxy=http://192.168.1.91:7890

python3.11 translate.py \
  --input /usr/src/WCC-doc/docs/source/locales/ja/LC_MESSAGES/client_菜单功能.po \
  --source zh-CN \
  --target ja \
  --output /usr/src/WCC-doc/tools/client_菜单功能_translated.po
```

## docx转md

```
pandoc source.docx -t markdown_strict -o target1.md --extract-media=./images

# 或

pandoc source.docx -t markdown_mmd -o target2.md --extract-media=./images
```

## 重置构建依赖

```
cd docs/source && pip3.11 freeze > requirements.txt
```

## 本地调试依赖

```
pip3.11 install -U sphinx

pip3.11 install sphinx-rtd-theme

pip3.11 install myst-parser

pip3.11 install sphinx-intl
```
