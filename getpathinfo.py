"""
getpathinfo.py 封装项目测试路径
Code description:配置文件路径
"""
import os

def get_path():
    # 获取当前路径
    curpath = os.path.dirname(os.path.realpath(__file__))
    return curpath

if __name__ == '__main__':  # 执行该文件，测试下是否OK
    print('测试路径是否OK,路径为：', get_path())
