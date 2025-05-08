import hashlib
import requests
import base64
import time
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime


class BaiduImageTranslator:
    def __init__(self, appid: str, secret_key: str):
        self.appid = appid
        self.secret_key = secret_key
        self.api_url = "https://fanyi-api.baidu.com/api/trans/sdk/picture"
        self.cuid = "APICUID"
        self.mac = "mac"
        self.version = "3"
        self.USE_COLOR = sys.stdout.isatty()
        self.total = 0
        self.success = 0
        self.failed = 0
        self.skip = 0


    def log(self, msg, level="info"):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        color = ""
        reset = "\033[0m" if self.USE_COLOR else ""

        if self.USE_COLOR:
            if level == "error":
                color = "\033[91m"  # 红色
            elif level == "success":
                color = "\033[92m"  # 绿色
            elif level == "warning":
                color = "\033[93m"  # 黄色

        print(f"{now} - {color}{msg}{reset}")


    def _validate_image(self, image_path: str) -> bool:
        try:
            ext = Path(image_path).suffix.lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                self.log(f"错误：不支持的图片格式 {ext}，仅支持jpg/jpeg/png")
                return False

            file_size = os.path.getsize(image_path) / (1024 * 1024)
            if file_size > 4:
                self.log(f"错误：图片大小 {file_size:.2f}MB 超过4MB限制")
                return False

            return True
        except Exception as e:
            self.log(f"图片验证失败: {str(e)}")
            return False


    def _generate_sign(self, image_data: bytes, salt: str) -> str:
        md5_image = hashlib.md5(image_data).hexdigest()
        sign_str = f"{self.appid}{md5_image}{salt}{self.cuid}{self.mac}{self.secret_key}"
        return hashlib.md5(sign_str.encode()).hexdigest()

    def translate_image(self, image_path: str, from_lang: str = "zh", to_lang: str = "en", paste_type: int = 1) -> dict:
        if not self._validate_image(image_path):
            return {"error": "Invalid image"}

        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()

            salt = str(int(time.time()))
            sign = self._generate_sign(image_data, salt)

            params = {
                "from": from_lang,
                "to": to_lang,
                "appid": self.appid,
                "salt": salt,
                "cuid": self.cuid,
                "mac": self.mac,
                "version": self.version,
                "sign": sign,
                "paste": paste_type,
                "needIntervene": 1
            }

            files = {'image': (Path(image_path).name, image_data, 'image/png')}
            response = requests.post(self.api_url, params=params, files=files)
            result = response.json()

            if result.get("error_code") == "0":
                return result
            else:
                return {"error": result.get("error_msg")}

        except Exception as e:
            return {"error": str(e)}

    def save_result_image(self, result: dict, output_path: str, paste_type: int):
        data = result.get("data", {})
        try:
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            if paste_type == 1 and data.get("pasteImg"):
                self._save_single_image(data["pasteImg"], output_path)
                self.log(f"整图翻译结果已保存：{output_path}", level="success")
                self.success += 1
            elif paste_type == 2 and data.get("content"):
                for idx, block in enumerate(data["content"]):
                    if block.get("pasteImg"):
                        block_image_path = os.path.join(output_dir, f"block_{idx}_translated.png")
                        self._save_single_image(block["pasteImg"], block_image_path)
                self.log(f"已保存 {len(data['content'])} 个分块翻译结果", level="success")
                self.success += 1
        except Exception as e:
            self.log(f"保存图片失败: {str(e)}", level="error")
            self.failed += 1

    @staticmethod
    def _save_single_image(base64_str: str, filename: str):
        if "," in base64_str:
            base64_str = base64_str.split(",")[1]

        img_data = base64.b64decode(base64_str)
        with open(filename, "wb") as f:
            f.write(img_data)


def process_images(input_dir: str, output_dir: str, appid: str, secret_key: str, from_lang: str, to_lang: str, paste_type: int, skip_existing: bool):
    exclude_dirs = {'en', 'ja'}
    exclude_files = {'favicon.png', 'logo.png'}

    translator = BaiduImageTranslator(appid, secret_key)

    # 判断是否是图片路径
    if Path(input_dir).is_file():
        image_paths = [input_dir]
    else:
        # 先统计所有图片路径
        image_paths = []
        for root, dirs, files in os.walk(input_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if file in exclude_files:
                    continue
                full_path = os.path.join(root, file)
                if Path(full_path).suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    image_paths.append(full_path)

    translator.total = len(image_paths)
    translator.success = 0
    translator.failed = 0
    translator.skip = 0

    translator.log(f"开始处理，总共可翻译图片数: {translator.total}")

    for idx, image_path in enumerate(image_paths):
        # 判断 input_dir 是否是文件
        if Path(input_dir).is_file():
            # 如果 input_dir 是文件，直接使用 image_path 作为相对路径
            output_image_path = Path(output_dir) / Path(image_path).name
        else:
            # 否则，按原先的逻辑处理相对路径
            relative_path = Path(image_path).relative_to(input_dir)
            output_image_path = Path(output_dir) / relative_path

        # 如果跳过已翻译的，检查输出路径是否已存在
        if skip_existing and output_image_path.exists():
            translator.log(f"已存在翻译结果，跳过：{output_image_path}", level="warning")
            translator.skip += 1
            continue

        translator.log(f"[{idx+1}/{translator.total}] 正在翻译: {image_path}")
        result = translator.translate_image(
            image_path=image_path,
            from_lang=from_lang,
            to_lang=to_lang,
            paste_type=paste_type
        )
        if "error" in result:
            translator.log(f"请求失败: {result['error']}", level="error")
            translator.failed += 1
        else:
            # 关键：保留原目录结构
            translator.save_result_image(result, str(output_image_path), paste_type)
    
    translator.log("翻译完成")
    translator.log(f"总数: {translator.total}，成功: {translator.success}，失败: {translator.failed}，跳过: {translator.skip}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Baidu Image Translator")
    parser.add_argument("appid", help="Baidu API APPID")
    parser.add_argument("secret_key", help="Baidu API Secret Key")
    parser.add_argument("input_dir", help="输入文件夹路径或图片路径")
    parser.add_argument("output_dir", help="输出文件夹路径，翻译后的图片将保存在此目录")
    parser.add_argument("from_lang", help="原语言（默认 zh）")
    parser.add_argument("to_lang", help="目标语言（默认 en）")
    parser.add_argument("paste_type", type=int, choices=[0, 1, 2], default=1, help="贴合类型：0-关闭，1-整图贴合，2-分块贴合")
    parser.add_argument("--skip_existing", action="store_true", help="跳过已翻译的图片")

    args = parser.parse_args()

    start_time = time.time()  # 记录开始时间
    process_images(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        appid=args.appid,
        secret_key=args.secret_key,
        from_lang=args.from_lang,
        to_lang=args.to_lang,
        paste_type=args.paste_type,
        skip_existing=args.skip_existing
    )
    end_time = time.time()    # 记录结束时间

    total_seconds = int(end_time - start_time)
    minutes, seconds = divmod(total_seconds, 60)
    print(f"程序总耗时: {minutes} 分 {seconds} 秒")
