#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import csv
import json
import pandas as pd

# json批处理转换xlsx
# 需要安装pandas

# 文件源位置
in_file = os.listdir('D:\Text')
# 创建循环，遍历每一个json文件
for i in in_file:
    # 读取json文件
    df = pd.read_json(r'D:/Textdlc/' + i)
    # 导出xlsx表格，也可以改成csv，生成的文件会有索引，如果不需要可以在末尾写index=false
    df.to_excel('D://out/' + i + ".xlsx",encoding="utf-8",index=false)

print('处理完成啦！')
