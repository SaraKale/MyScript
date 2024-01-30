# ========================
# 将评论数据中的"Comment"块提取"insertedAt"日期时间按照正则表达式排列为正序
# 以最早的时间在前，最新时间在后
# ========================

import json
import re

def extract_insertedAt(comment):
    # 使用正则表达式提取 "insertedAt" 的日期时间部分
    match = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z', comment["insertedAt"])
    return match.group() if match else None

def sort_comments_by_insertedAt(json_data):
    # 从整个JSON数据块中提取并排序 "insertedAt"
    sorted_json_data = sorted(json_data["data"]["Comment"], key=extract_insertedAt)

    # 更新原始数据
    json_data["data"]["Comment"] = sorted_json_data

# 指定输入和输出文件路径
input_file_path = 'waline.json'
output_file_path = 'waline-output.json'

# 从输入文件读取JSON数据
with open(input_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 调用函数进行排序
sort_comments_by_insertedAt(data)

# 将结果写入输出文件，禁用Unicode转义
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

print(f"数据已按照 'insertedAt' 的日期时间正序排序，并保存到文件: {output_file_path}")
