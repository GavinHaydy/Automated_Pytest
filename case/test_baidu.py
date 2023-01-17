import pytest
from page.Home import HomePage


class TestDome(object):
    def test_one(self, drivers):
        s = HomePage(drivers)
        s.search_input('python')
        s.search_button()
        print(s.test_a())
        pytest.assume(s.title() == 'baidu')
