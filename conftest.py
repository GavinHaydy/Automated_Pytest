import os
import allure
import pytest
from selenium import webdriver
from common.log import AutoTestLog

"""function：每一个函数或方法都会调用
class：每一个类调用一次，一个类中可以有多个方法
module：每一个.py文件调用一次，该文件内又有多个function和class
session：是多个文件调用一次，可以跨.py文件调用，每个.py文件就是module"""

driver = None


@pytest.fixture(scope='session', autouse=True)
def drivers():
    """前置操作——登录"""
    global driver
    if driver is None:
        driver = webdriver.Chrome()
        driver.get('D:/data/ZDH/baidu.html')
    yield driver
    driver.quit()


@pytest.fixture(scope='class', autouse=True)
def start_log():
    """日志记录"""
    log = AutoTestLog('error')
    logger = log.get_log()
    yield
    log.close_handle()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """失败用例截图"""
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            if "tmpir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
                f.write(rep.nodeid + extra + "\n")
            with allure.step('失败截图'):
                allure.attach(driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)
