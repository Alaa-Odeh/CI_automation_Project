from selenium.webdriver.common.by import By

from logic.web_logic.learning_pages import LearningPages

class MyPathPage:
    BACKEND_COURSE_LINKS='(//div[@class="chakra-stack css-d3x6qa"])[1]//a'

    def __init__(self,driver):
        self.driver =driver
        self.backend_course_links=self.driver.find_elements(By.XPATH,self.BACKEND_COURSE_LINKS)
        self.learning_pages=LearningPages(self.driver)
        self.path_labels=[]
        self.actuall_labels=[]
    def click_backend_course_link(self,link):
        self.backend_course_links[link].click()

    def click_backend_course_links_and_get_pages_labels(self):
        for link in self.backend_course_links:
            label = self.backend_course_links[link].find_element_by_tag_name('p').text
            if label=="Practice Quiz":
                pass
            else:
                self.click_backend_course_link(link)
                self.actuall_labels.append(self.learning_pages.get_course_label_in_the_right_formate(label))

    def get_backend_courser_labels_from_my_path(self):
        for link in self.backend_course_links:
            label = self.backend_course_links[link].find_element_by_tag_name('p').text
            if label=="Practice Quiz":
                pass
            else:
                self.path_labels.append(label)

    def get_actuall_page_labels_on_both_websites(self):
        self.click_backend_course_links_and_get_pages_labels()
        self.get_backend_courser_labels_from_my_path()


