# 将waline评论数据json文件拆分，按每100块数据拆分成多个小文件
# 将会拆分"Comment", "Users", "Counter"三个表，请自己看情况更改。

import json
import os  # 添加os模块用于处理路径

def split_data(input_file, output_path, output_prefix, chunk_size, table_name):
    # 读取JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 获取指定表的数据
    table_data = data["data"].get(table_name, [])

    # 计算总行数和拆分块数
    total_rows = len(table_data)
    num_chunks = total_rows // chunk_size

    # 遍历拆分块
    for i in range(num_chunks + 1):
        start_index = i * chunk_size
        end_index = min((i + 1) * chunk_size, total_rows)

        # 构建输出文件名
        output_file = os.path.join(output_path, f"{output_prefix}_{table_name}_{start_index + 1}_{end_index}.json")

        # 打开输出文件并写入拆分后的数据
        with open(output_file, 'w', encoding='utf-8') as f_out:
            chunk_data = {
                "__version": data["__version"],
                "type": data["type"],
                "version": data["version"],
                "time": data["time"],
                "tables": data["tables"],
                "data": {
                    table_name: table_data[start_index:end_index]
                }
            }
            json.dump(chunk_data, f_out, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # 输入文件名
    input_file = "waline.json"
    
    # 输出路径
    output_path = "output_files"
    
    # 输出文件名前缀
    output_prefix = "output_chunk"

    # 指定每个文件包含的数据个数，比如拆分每100块数据
    chunk_size = 100  

    # 需要拆分的表名列表
    tables_to_split = ["Comment", "Users", "Counter"]  

    # 遍历需要拆分的表
    for table_name in tables_to_split:
        split_data(input_file, output_path, output_prefix, chunk_size, table_name)
