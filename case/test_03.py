from page.Two import TwoPage


class TestDemo1:
    def test_12(self, drivers):
        s = TwoPage(drivers)
        s.search_input('selenium')
        s.search_button()
