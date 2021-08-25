import os

# 当前目录
current_path = os.getcwd() + '\\resources'

# resources列表
attribute_path = current_path + "\\attributes"
disambiguation_path = current_path + "\\disambiguation"
instance_path = current_path + "\\instances"
relations_path = current_path + "\\relations"
types_path = current_path + "\\types"
user_dicts = current_path + "\\user_dicts"

if __name__ == '__main__':
    print(open(instance_path,encoding="utf-8").readlines())