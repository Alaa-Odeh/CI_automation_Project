from infra.infra_web.base_page import BasePage


class SvgTutorial(BasePage):

    def __init__(self,driver):
        super().__init__(driver)

    def get_page_header(self):
        self.header=self.get_header().text


