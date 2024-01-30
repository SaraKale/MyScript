# 在/blog/posts/末尾插入斜杠/
# 使用正则表达式才能匹配到

import re
import json

def process_json(input_file, output_file):
    # 从输入文件读取JSON数据
    with open(input_file, 'r', encoding='utf-8') as file:
        json_data = file.read()

    # 在"/blog/posts/ 后的双引号前插入斜杠
    modified_json_data = re.sub(r'("/blog/posts/[^"]*)",', r'\1/",', json_data)

    # 将修改后的数据写入输出文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(modified_json_data)

# 设置输入文件和输出文件的路径
input_file_path = 'waline.json'  # 你的输入文件路径
output_file_path = 'waline-out.json'  # 你的输出文件路径

# 调用函数处理JSON数据
process_json(input_file_path, output_file_path)

print(f"处理完成。请查看输出文件: {output_file_path}")
