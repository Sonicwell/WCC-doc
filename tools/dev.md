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
  --input /usr/src/WCC-doc/docs/source/locales/ja/LC_MESSAGES/client_系统登录.po \
  --source zh-CN \
  --target ja \
  --output /usr/src/WCC-doc/tools/client_系统登录_translated.po
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

## 文档编写时的注意事项

```
1 文档使用Markdown语法，参考 https://markdown.com.cn/basic-syntax

2 所有文档只能放到 docs/source 目录下，不要建立子目录存放，否则下载的文档，无法加载图片。

3 当有新增文档要放入菜单树时，参见 docs/source/index.rst 中的其他文档写法。

4 图片都放到 docs/source/_static/images 目录下，你可以在其下构建每个文档的目录，这样便于管理。

5 图片引入语法统一使用 ![alt text](_static/images/client/media/image24.png)
  图片要单独占一行，不要和文字同行。

6 图片多语言目录为 _static/images/en 和 _static/images/ja，默认 _static/images 下面放中文图片。
  多语言图片子目录要保持路径、文件名称一致。举例：
  _static/images/client/media/image24.png、
  _static/images/ja/client/media/image24.png、
  _static/images/en/client/media/image24.png 
  是三张指代同一内容，但不同语言的图片。

7 文档标题最高可用二级标题，即 ## xxxxx。一级标题 # xxx 为文档框架保留使用，你不要使用。

8 段落间要留有一行空行(或段落结尾留有2个空格，推荐使用空行分割更保险)，否则页面渲染时，两行会连成一行显示。

9 加粗使用 **xxx**，两头都不要有空格，两头也不要用中文符号。即不要写成 ** xxx ***，也不要写成**xxx：***，这会导致加粗失败。

10 加粗的*前后要留有空格，否则会导致解析失败。正确写法如 xxxx **yyy** xxxx。

11 以数字开头的段落，不要用.或)接文字。如 1. xxx、 2. xxx、 1）xxx、2) xxx，这样会导致多语言翻译无法被渲染解析。
   应写成 1 xxx、 2 xxx、 ① xxx、② xxx。
   备用符号: ① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩
```
