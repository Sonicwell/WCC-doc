## po文件更新

```
cd docs/source

sphinx-build -b gettext . _build/gettext

sphinx-intl update -p _build/gettext -l en -l ja -l zh_CN
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
