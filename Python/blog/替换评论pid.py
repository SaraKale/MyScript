# 替换评论的pid数值为comment (#)里面的值，针对Leancloud数据库早期评论的pid值替换
# \d+ 用于匹配一个或多个数字字符
# \S+ 来匹配非空白字符，不仅限于数字，也可能包含其他字符

import re
import json

def replace_pid_with_comment(json_file_path, output_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 获取Comment表中的数据
    comment_data = data.get('data', {}).get('Comment', [])

    for entry in comment_data:
        pid_value = entry.get('pid')
        comment_value = entry.get('comment')

        if pid_value and comment_value:
            # 使用正则表达式提取"pid"后面的数值
            pid_match = re.search(r'"pid":\s*"(\S+)"', json.dumps(entry))
            if pid_match:
                pid_number = pid_match.group(1)

                # 替换到"comment"后面的(#)里面，保留#，同时转义括号
                entry['comment'] = re.sub(r'(?<=\(#)\S+(?=\))', pid_number, comment_value)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, ensure_ascii=False, indent=2)

# 替换json文件中的"pid"到"comment"中
# 填写输入文件、输出文件
replace_pid_with_comment('waline.json', 'waline-output.json')

print(f"数据已替换成功，并保存到文件: {output_file_path}")