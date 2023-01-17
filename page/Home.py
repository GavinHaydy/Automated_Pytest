from selenium.webdriver.common.by import By

from common.Base import Base


class HomePage(Base):

    def search_input(self, text=None):
        self.send_keys(('id', 'kw'), text)

    def search_button(self):
        self.click(('id', "su"))

    def text_p(self):
        return self.get_element_value(('id', 'kw'))

    def title(self):
        return self.get_title()

    def test_a(self):
        return self.is_element_exist(('id', 'asdf'))
