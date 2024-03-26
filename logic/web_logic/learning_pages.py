from selenium.webdriver.common.by import By


class LearningPages:


    def __init__(self,driver):
        self.driver =driver

    def get_course_label_in_the_right_formate(self,label):
        COURSE_LABELS = f'// div[ @ id = "leftmenuinnerinner"] // a[contains(text(), {label})]'
        self.course_labels=self.driver.find_element(By.XPATH,COURSE_LABELS)
        return self.course_labels.text().capitalize()

    def scroll_down_to_mimic_reading_page(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.back()