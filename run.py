"""
Code description: 运行测试用例
"""
import pytest
import os
import shutil
import getpathinfo

if __name__ == '__main__':
    path = getpathinfo.get_path()  # 获取本地路径
    report_path = os.path.join(path, 'report')
    # 判断report文件夹是否存在，不存在就自动创建一个
    if not os.path.exists(report_path):
        os.mkdir(report_path)
    try:
        # 删除之前的文件夹
        shutil.rmtree("report")
        print('清除之前报告')
    finally:
        print('清理完成')
    pytest.main(['--alluredir', '.pytest_cache/json'])
    # 直接生成报告html文件
    os.system('allure generate .pytest_cache/json -o ./report --clean')
