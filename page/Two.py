from selenium.webdriver.common.by import By

from common.Base import Base


class TwoPage(Base):
    url = 'www.baidu.com'

    def search_input(self, text=None):
        self.send_keys((By.ID, 'kw'), text)

    def search_button(self):
        self.click((By.ID, "su"))

    def text_p(self):
        return self.get_element_value(('id','kw'))