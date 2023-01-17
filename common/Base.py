"""
文件名:Base.py
作用:对selenium进行二次封装
"""

import os
import re
# 导包
import traceback

from selenium import webdriver
from selenium.common import NoSuchElementException, NoSuchFrameException, InvalidSelectorException, \
    UnknownMethodException, InvalidArgumentException
from selenium.webdriver import ActionChains, DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from common.log import AutoTestLog


# opt = webdriver.ChromeOptions()
# opt.add_argument('--user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data')  # 读取本地chrome配置


def open_browser(browser='Chrome', **kwargs):  # 不输入参数,默认打开谷歌浏览器
    """
    通过浏览器名称,打开对应的浏览器
    :param browser: 浏览器名称
    :return: driver,即webdriver.browser()
    """
    if browser.capitalize() == 'Chrome':
        if kwargs.get('logs'):
            caps = DesiredCapabilities.CHROME
            caps['loggingPrefs'] = {
                'browser': 'ALL',
                'performance': 'ALL'
            }
            caps['perfLoggingPrefs'] = {
                'enableNetwork': True,
                'enablePage': False,
                'enableTimeline': False
            }
            option = webdriver.ChromeOptions()
            option.add_argument('--no-sandbox')
            option.add_experimental_option('w3c', True)
            driver = webdriver.Chrome(desired_capabilities=caps, options=option)
        else:
            driver = webdriver.Chrome(**kwargs)
    elif browser.capitalize() == 'Firefox':
        driver = webdriver.Firefox()
    elif browser.capitalize() == 'Edge':
        driver = webdriver.Edge()
    else:
        raise Exception('请输入正确的浏览器名称,例如Chrome,Firefox,Edge')
    return driver


class Base(object):
    def __init__(self, driver):  # 将打开浏览器的返回值driver,即webdriver.browser()传进来
        self.driver = driver
        self.log = AutoTestLog('warning')

    def open_url(self, url):
        """
        进入网页
        :param url: 网页域名
        :return:
        """
        try:
            if url.startswith('http://') or url.startswith('https://'):
                self.driver.get(url)
                self.driver.maximize_window()  # 浏览器窗口最大化
            else:
                self.driver.get('http://' + url)
        except UnknownMethodException:
            print('浏览器打开失败,无法输入网址')

    def quit_browser(self):
        """
        退出浏览器
        :return:
        """
        self.driver.quit()

    def close_browser(self):
        """
        关闭浏览器
        :return:
        """
        self.driver.close()

    def _find_element(self, locator: tuple, timeout: int = 10):
        """
        找单个元素
        :param locator:元素定位器,数据类型是元组
        :param timeout:最大等待时间,默认为10s
        :return:如果元素存在,返回元素本身,反之返回False
        """
        dyz = traceback.extract_stack()[-2]
        try:
            # 显式等待和EC模块联用,定位单个元素
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
        except NoSuchElementException:
            self.log.logger.error(
                f'{os.path.basename(dyz.filename), dyz.lineno, dyz.name}-元素{locator}没有找到')
            return False

    def _find_elements(self, locator: tuple, timeout: int = 10):
        """
        找元素的复数形式
        :param locator:元素定位器,数据类型是元组
        :param timeout:最大等待时间,默认为10s
        :return:如果元素存在,返回元素本身,反之返回False
        """
        dyz = traceback.extract_stack()[-2]
        try:
            # 显式等待和EC模块联用,定位元素的复数形式
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))
        except NoSuchElementException:
            self.log.logger.error(
                f'{os.path.basename(dyz.filename), dyz.lineno, dyz.name}-元素{locator}没有找到')
            return False

    def send_keys(self, locator, text):
        """
        元素中输入内容
        :param locator:元素定位器,数据类型是元组
        :param text:输入的内容
        :return:
        """
        dyz = traceback.extract_stack()[-2]
        try:
            element = self._find_element(locator)  # 定位元素
            element.clear()  # 清空输入框
            element.send_keys(text)  # 输入内容
        except InvalidArgumentException:
            self.log.logger.error(
                f'{os.path.basename(dyz.filename), dyz.lineno, dyz.name}-元素{locator}没有找到,无法输入内容')

    def click(self, locator):
        """
        点击元素
        :param locator:元素定位器,数据类型是元组
        :return:
        """
        dyz = traceback.extract_stack()[-2]
        try:
            self._find_element(locator).click()  # 点击元素
        except InvalidArgumentException:
            self.log.logger.error(
                f'{os.path.basename(dyz.filename), dyz.lineno, dyz.name}-元素{locator}没有找到,无法点击'
            )

    def get_title(self):
        return self.driver.title

    def get_element_text(self, locator):
        """
        获取元素文本值
        :param locator: 元素定位器,数据类型是元组
        :return:
        """
        dyz = traceback.extract_stack()[-2]
        try:
            element = self._find_element(locator)  # 定位元素
            return element.text  # 获取元素文本值
        except InvalidArgumentException:
            print(f'{os.path.basename(dyz.filename), dyz.lineno, dyz.name}-元素{locator}没有找到,无法获取文本值')

    def get_element_value(self, locator):
        """
        获取元素的value属性值
        :param locator: 元素定位器,数据类型是元组
        :return:
        """
        dyz = traceback.extract_stack()[-2]
        try:
            element = self._find_element(locator)  # 定位元素
            return element.get_attribute('value')  # 获取元素value属性值
        except InvalidArgumentException:
            print(f'{os.path.basename(dyz.filename), dyz.lineno, dyz.name}-元素{locator}没有找到,无法获取value属性值')

    def is_selected(self, locator):
        """判断元素是否被选中，返回bool值"""
        return self._find_element(locator).is_selected()

    def is_element_exist(self, locator):
        """是否找到"""
        try:
            self._find_element(locator)
            return True
        except:
            return False

    def select(self, locator):
        """
        下拉框选项选取
        :param locator: 下拉框定位器,数据类型是元组
        :return:
        """
        try:
            select = Select(self._find_element(locator))  # 创建一个Select类
            # select.select_by_index(index)   #通过索引选择选项
            return select
        except InvalidSelectorException:
            print(f'元素{locator}没有找到,无法进行选择')

    def in_iframe(self, param):
        """
        进入iframe
        :param param: ①有id/name属性时,param为id/name属性值;②没有时,自己加上locator,locator为元组;③索引值.索引从0开始
        :return:
        """
        try:
            self.driver.switch_to.frame(param)  # 进入iframe
        except NoSuchFrameException:
            print(f'{param}没有找到,无法进入iframe')

    def switch_iframe(self, id_index_locator):
        """切换iframe"""
        try:
            if isinstance(id_index_locator, int):
                self.driver.switch_to.frame(id_index_locator)
            elif isinstance(id_index_locator, str):
                self.driver.switch_to.frame(id_index_locator)
            elif isinstance(id_index_locator, tuple):
                self.driver.switch_to.frame(self._find_element(id_index_locator))
        except NoSuchFrameException:
            self.log.logger.error("iframe切换异常")

    def out_iframe(self):
        """
        退出iframe
        :param driver: driver=open_browser()
        :return:
        """
        self.driver.switch_to.default_content()  # 返回最外层

    def select_by_index(self, locator, index=0):
        """通过索引，index是索引第几个，从0开始，默认第一个"""
        Select(self._find_element(locator)).select_by_index(index)

    def clear_text(self, locator):
        """
        清空输入框内容
        :param locator: 定位器,元组
        :return:
        """
        try:
            element = self._find_element(locator)  # 定位元素
            return element.clear()  # 清空输入框内容
        except:
            print(f"元素{locator}没有找到,无法清空输入框内容")

    def roller(self, vertical: int, hor: int = 10):
        """
        滚轮向下滚动
        :param hor: 水平距离,默认为0
        :param vertical:垂直距离
        :return:
        """
        js_down = f'window.scrollTo({hor},{vertical});'  # js代码
        self.driver.execute_script(js_down)  # 执行js代码

    def back(self):
        """浏览器后退"""
        self.driver.back()

    def click_alert(self):
        """
        捕获弹窗,点击确定
        :return:
        """
        alert = self.driver.switch_to.alert  # 捕获弹窗
        alert.accept()  # 点击确定按钮

    def js_execute(self, js):
        """
        执行js代码
        :param js: 需要被执行的js语句
        :return:
        """
        self.driver.execute_script(js)

    def is_displayed(self, locator):
        """判断元素是否存在"""
        try:
            return self._find_element(locator).is_displayed()
        except:
            return False

    def js_focus_element(self, locator):
        """聚焦元素"""
        target = self._find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)

    def js_scroll_top(self):
        """滚到顶部"""
        js = "window.scrollTo(0,0)"
        self.driver.execute_script(js)

    def js_scroll_end(self, x=0):
        """滚到底部"""
        js = "window.scrollTo(%s, document.body.scrollHeight)" % x
        self.driver.execute_script(js)

    def move_to_element(self, locator):
        """鼠标悬停操作"""
        ele = self._find_element(locator)
        ActionChains(self.driver).move_to_element(ele).perform()

    def implicit(self, time_out: int = 5):
        """隐式等待"""
        self.driver.implcititly_wait(time_out)

    def refresh(self):
        """刷新浏览器"""
        self.driver.refresh()
