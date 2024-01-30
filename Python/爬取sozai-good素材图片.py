# ------------------------------------------
# 爬取sozai-good上的素材图片 https://sozai-good.com
#
# 需要安装：
# pip install requests
# pip install beautifulsoup4
# 如果出现了SSL/TLS错误，需要更新：
# pip install --upgrade requests
# 
# 下载较慢，需要全局挂梯子
# ------------------------------------------

import os
import requests
import time
import re
import json
import signal
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from urllib.parse import urljoin

# 全局变量保存已下载的链接
downloaded_files = set()

def signal_handler(signal, frame):
    # 处理终止信号
    print("正在保存文件中...")
    save_downloaded_files(output_folder, downloaded_files)
    sys.exit(0)

# 注册信号处理函数
signal.signal(signal.SIGINT, signal_handler)

def download_file(base_url, output_folder, material_div, downloaded_files):

    # 获取图片下载链接
    link = material_div.find('a')
    image_page_url = urljoin(base_url, link['href'])

    # 发送HTTP请求获取图片页面内容
    image_page_response = requests.get(image_page_url)
    image_page_soup = BeautifulSoup(image_page_response.text, 'html.parser')

    # 查找包含指定下载类型的<span>元素
    download_types = image_page_soup.find_all('span', class_='material_download_name')
    for download_type in download_types:
        # 指定需要下载的类型
        target_types = ['AI(ベクター)', 'EPS(ベクター)', 'PSD(Photoshop)']
        if download_type.text.strip() in target_types:
            # 查找关联的下载按钮
            download_button = download_type.find_next('div', class_='material_download_button')

            if download_button:
                # 从data-href中提取下载链接信息
                data_href = download_button['data-href']
                download_info = re.search(r'id=(\d+)&type=(\d+)&subnumber=(\d+)&extention=(\w+)', data_href)

                if download_info:
                    id, type, subnumber, extention = download_info.groups()

                    # 构建下载链接
                    full_download_url = f"https://sozai-good.com/download?id={id}&type={type}&subnumber={subnumber}&extention={extention}"

                    # 获取图片名称
                    image_name_element = material_div.find('div', class_='materials_thumbnail_name')
                    if image_name_element:
                        image_name = image_name_element.text.strip()

                        # 构建本地文件路径
                        local_file_path = get_local_file_path(output_folder, image_name, extention)

                        # 检查文件是否已经下载过，如果是则跳过
                        if local_file_path in downloaded_files:
                            print(f"跳过 {image_name} ({download_type.text.strip()}), 文件已下载.")
                            continue

                        # 发送HTTP请求下载文件，添加重试逻辑
                        max_retries = 3
                        for attempt in range(max_retries):
                            try:
                                file_content = requests.get(full_download_url).content

                                # 写入文件
                                with open(local_file_path, 'wb') as file:
                                    file.write(file_content)

                                # 下载结果输出
                                print(f"Download {image_name} ({download_type.text.strip()}) to {local_file_path}")

                                # 将下载过的文件路径添加到已下载文件列表中
                                downloaded_files.add(local_file_path)

                                # 休眠5秒
                                time.sleep(5)

                                # 跳出重试循环
                                break
                            except requests.RequestException as e:
                                print(f"下载失败，正在进行第 {attempt + 1}/{max_retries} 次重试. 错误信息: {e}")
                                time.sleep(5)  # 等待5秒后重试
                    else:
                        print("在页面上找不到 materials_thumbnail_name 元素。")


# 获取本地文件路径
def get_local_file_path(output_folder, image_name, extention):
    image_name = clean_filename(image_name)
	# 打印文件名
    # print(f"Cleaned image name: {image_name}")
    if extention.lower() == 'ai':
        return os.path.join(output_folder, f"{image_name}.ai")
    elif extention.lower() == 'eps':
        return os.path.join(output_folder, f"{image_name}.eps")
    elif extention.lower() == 'psd':
        return os.path.join(output_folder, f"{image_name}.psd")
    else:
        return os.path.join(output_folder, f"{image_name}.zip")

# 清理文件名无效字符
# Windows文件系统中不允许文件名包含以下字符：
# \ / : * ? " < > |
def clean_filename(filename):
    # 无效字符列表，包括 Windows 文件系统不允许的字符
    invalid_chars = r'\/:*?"<>|'
    
    # 替换无效字符为下划线
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # 移除其他可能导致问题的字符
    invalid_filename_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    filename = ''.join(c for c in filename if c not in invalid_filename_chars)

    return filename

def get_total_pages(soup):
    # 不再需要获取总页数
    return 1

# 读取下载列表
def load_downloaded_files(output_folder):
    downloaded_files_path = os.path.join(output_folder, "downloaded_files.json")

    if os.path.exists(downloaded_files_path):
        with open(downloaded_files_path, 'r') as file:
            return set(json.load(file))  # 将列表转换为集合
    else:
        return set()

# 保存下载列表
def save_downloaded_files(output_folder, downloaded_files):
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    downloaded_files_path = os.path.join(output_folder, "downloaded_files.json")

    with open(downloaded_files_path, 'w') as file:
        json.dump(list(downloaded_files), file)

# 主函数
def main():
    # 目标网页的URL
    base_url = input("请输入目标URL: ")  # 用户输入目标URL
    max_pages = int(input("请输入最大页数: "))  # 用户输入最大页数
    output_folder = "c:/out"  # 设置输出文件夹

    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 获取已下载的文件列表
    downloaded_files = load_downloaded_files(output_folder)

    # 注册信号处理函数
    signal.signal(signal.SIGINT, signal_handler)

    try:
        # 执行主要逻辑
        for page_num in range(1, max_pages + 1):
            page_url = f"{base_url}&page={page_num}"
            response = requests.get(page_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # 查找所有包含下载链接的<div>元素
            material_divs = soup.find_all('div', class_='category_material materials_thumbnail')

            # 遍历每个<div>元素
            for material_div in material_divs:
                download_file(base_url, output_folder, material_div, downloaded_files)

        # 保存已下载的文件列表
        save_downloaded_files(output_folder, downloaded_files)

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 终止时保存文件
        print("正在保存文件中...")
        save_downloaded_files(output_folder, downloaded_files)

if __name__ == "__main__":
    main()
