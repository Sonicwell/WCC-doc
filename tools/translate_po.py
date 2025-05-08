import polib
import requests
import re
import argparse
import os
import time
import sys
from datetime import datetime

# 项目文档根目录
PROJECT_ROOT = "/usr/src/WCC-doc/docs/source"

USE_COLOR = sys.stdout.isatty()

def log(msg, level="info"):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    color = ""
    reset = "\033[0m" if USE_COLOR else ""

    if USE_COLOR:
        if level == "error":
            color = "\033[91m"  # 红色
        elif level == "success":
            color = "\033[92m"  # 绿色
        elif level == "warning":
            color = "\033[93m"  # 黄色

    print(f"{now} - {color}{msg}{reset}")


# Google 翻译  zh-CN en ja auto
def translate_text(text, source_lang="zh-CN", target_lang="en"):
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": source_lang,  # 源语言
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
#img_pattern = re.compile(r'<img\s+[^>]*src=[\'"][^\'"]+[\'"][^>]*>', re.IGNORECASE)
img_pattern = re.compile(r'<img\s+[^>]*src=[\'"]([^\'"]+)[\'"][^>]*>', re.IGNORECASE)

# Markdown 格式图片 ![alt text](_static/images/root/media/image1.png)
#markdown_img_pattern = re.compile(r'!\[[^\]]*\]\([^\)]+\)', re.IGNORECASE)
markdown_img_pattern = re.compile(r'!\[[^\]]*\]\(([^)]+)\)', re.IGNORECASE)


def process_po_file(input_file, source_lang, target_lang, output_file, mode):
    if not os.path.exists(input_file):
        log(f"输入文件不存在: {input_file}")
        return

    po = polib.pofile(input_file)

    total_entries = len(po)
    log(f"总条目数: {total_entries}")

    processed_count = 0
    skip_img_count = 0
    skip_translated_count = 0
    success_count = 0
    failed_count = 0

    # 遍历所有条目，翻译未翻译的部分
    for index, entry in enumerate(po, start=1):
        if entry.occurrences and len(entry.occurrences[0]) == 2:
            line_number = entry.occurrences[0][1]
        else:
            line_number = "未知"

        if not entry.translated():  # 只处理未翻译的条目
            if img_pattern.search(entry.msgid) or markdown_img_pattern.search(entry.msgid):  # 如果是图片
                # 获取图片路径
                match = img_pattern.search(entry.msgid) or markdown_img_pattern.search(entry.msgid)
                img_path = match.group(1) if match else None

                if img_path:
                    # 插入语言目录到路径中
                    target_img_path = img_path.replace("_static/images/", f"_static/images/{target_lang}/")
                    
                    # 绝对路径检查用来判断文件是否存在
                    absolute_target_img_path = os.path.join(PROJECT_ROOT, target_img_path)
                    if os.path.exists(absolute_target_img_path):
                        entry.msgstr = f"![alt text]({target_img_path})"
                        log(f"[{index}/{total_entries}] 更新图片条目: {entry.msgid} -> {entry.msgstr} （位置: {line_number}）")
                        success_count += 1
                    else:
                        entry.msgstr = ""  # 如果不存在，保持为空
                        log(f"[{index}/{total_entries}] 图片不存在，保持为空: {entry.msgid} （位置: {line_number}）")
                        skip_img_count += 1
                else:
                    entry.msgstr = ""  # 如果没有匹配到图片路径，保持为空
                    log(f"[{index}/{total_entries}] 无法解析图片路径，保持为空: {entry.msgid} （位置: {line_number}）")
                    skip_img_count += 1
            elif mode != 'image':
                translated_text = translate_text(entry.msgid, source_lang, target_lang)
                if translated_text:  # 只有成功翻译才填充
                    entry.msgstr = translated_text
                    log(f"[{index}/{total_entries}] 翻译: {entry.msgid} -> {translated_text} （位置: {line_number}）", level="success")
                    success_count += 1
                else:
                    entry.msgstr = ""  # 保持为空
                    log(f"[{index}/{total_entries}] 翻译失败, msgstr保持为空: {entry.msgid} （位置: {line_number}）", level="error")
                    failed_count += 1
        else:
            log(f"[{index}/{total_entries}] 已翻译，跳过: {entry.msgid} （位置: {line_number}）")
            skip_translated_count += 1

        processed_count += 1

    # 保存回 PO 文件
    po.save(output_file)
    log(f"翻译完成，共处理 {processed_count} 条，已保存到 {output_file}")
    print(f"翻译成功数: {success_count} 条")
    print(f"翻译失败数: {failed_count} 条")
    print(f"跳过图片数: {skip_img_count} 条")
    print(f"跳过已译数: {skip_translated_count} 条")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PO 文件翻译器（基于 Google Translate）")
    parser.add_argument('--input', required=True, help="输入 PO 文件路径")
    parser.add_argument('--source', default='zh-CN', help="源语言代码，默认 zh-CN，自动检测 auto")
    parser.add_argument('--target', required=True, help="目标语言代码，例如 zh-CN en ja")
    parser.add_argument('--output', required=True, help="输出翻译后 PO 文件路径")
    parser.add_argument('--mode', choices=['default', 'image'], default='default', help="模式：default（翻译所有条目），image（只处理图片条目）")

    args = parser.parse_args()

    start_time = time.time()  # 记录开始时间
    process_po_file(args.input, args.source, args.target, args.output, args.mode)
    end_time = time.time()    # 记录结束时间

    total_seconds = int(end_time - start_time)
    minutes, seconds = divmod(total_seconds, 60)
    log(f"程序总耗时: {minutes} 分 {seconds} 秒")
