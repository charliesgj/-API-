import json
import re
# 将字典写入文件
def write_to_file(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file)

# 从文件中读取字典
def read_from_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        return data

