import json
import re
import time
from pathlib import Path
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GoalsWeb():
    MY_GOALS="//h2[contains(text(),'My Goals')]/following-sibling::*[1]"
    CONTINUE_BUTTON='//button[contains(text(),"Continue")]'
    ADD_ADDITIONAL_SKILLS_BUTTON='//button[./*[contains(text(),"Add additional skills")]]'
    HOURS_SLIDER='//*[@id="slider-thumb-slider-duration"]'
    CREATE_BUTTON='//button[contains(text(),"Create")]'
    RESUME_LEARNING_BUTTON='//div[@class="css-13htum"]'
    UPPER_FRAME='//iframe[@id="top-nav-bar-iframe"]'
    UPDATE_GOAL='//button[contains(text(),"Update")]'
    DELETE_GOAL='//button[contains(text(),"Delete")]'
    FOOTER_DELETE="//footer//button[contains(text(), 'Delete')]"
    def __init__(self, driver):
        self._driver =driver
        wait = WebDriverWait(driver, 20)  # Timeout of 10 seconds
        cur_dir = Path(__file__).resolve().parents[0].parents[0].joinpath("Info_API.json")
        with open(cur_dir, 'r') as config_file:
            self.info_api = json.load(config_file)

    def init(self):
        self.add_a_goal_button=WebDriverWait(self._driver, 15).until(EC.visibility_of_element_located((By.XPATH, self.MY_GOALS)))


    def click_on_add_a_goal_button(self,goal_name):
        self.add_a_goal_button.click()
        self.goal_name_button=WebDriverWait(self._driver,15).until(EC.visibility_of_element_located((By.XPATH, f'//button[contains(text(),"{goal_name}")]')))

    def click_on_goal_name_button(self):
        self.goal_name_button.click()
        self.continue_button=self._driver.find_element(By.XPATH, self.CONTINUE_BUTTON)

    def click_on_continue_button(self):
        self.continue_button.click()
        self.add_additional_skills_button = WebDriverWait(self._driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.ADD_ADDITIONAL_SKILLS_BUTTON)))

    def click_on_add_additional_skills_button(self,):
        self.add_additional_skills_button.click()

    def locate_edit_goal_button(self,goal_name):
        self.goal_edit_button=WebDriverWait(self._driver, 15).until(EC.element_to_be_clickable((By.XPATH, f'//p[contains(text(),"{goal_name}")]/following-sibling::*[1]')))

    def click_on_edit_goal_button(self):
        self.goal_edit_button.click()
        self.update_goal_button=WebDriverWait(self._driver,15).until(EC.element_to_be_clickable((By.XPATH, self.UPDATE_GOAL)))
        self.add_additional_skills_button = WebDriverWait(self._driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.ADD_ADDITIONAL_SKILLS_BUTTON)))
        self.delete_goal_button = WebDriverWait(self._driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.DELETE_GOAL)))
    def click_on_update_goal_button(self):
        self.update_goal_button.click()

    def click_on_delete_goal_button(self):
        self.delete_goal_button.click()
        self.footer_delete=WebDriverWait(self._driver, 15).until(EC.element_to_be_clickable((By.XPATH, self.FOOTER_DELETE)))

    def click_on_footer_delete_button(self):
        self.footer_delete.click()
    def make_changes(self,goal_name,chosen_skills,courses_levels,hours_weekly):
        self.locate_edit_goal_button(goal_name)
        self.click_on_edit_goal_button()
        self.click_on_add_additional_skills_button()
        for skill, level in zip(chosen_skills, courses_levels):
            self.click_on_skills_checkbox(skill)
            self.set_course_level_to_your_choice(level)
        self.set_hours_weekly_slider(hours_weekly)
        self.click_on_update_goal_button()
    def click_on_skills_checkbox(self,chosen_skill):
        labels = f'//label[./span[contains(text(),"{chosen_skill}")]]//span'
        self.skills_checkbox = self._driver.find_elements(By.XPATH, labels)[0]
        self.skills_checkbox.click()
        self.course_level_button = WebDriverWait(self._driver, 15).until(EC.visibility_of_element_located((By.XPATH, f'//div[./div[./div[./p[contains(text(),"{chosen_skill}")]]]]//select')))

    def set_course_level_to_your_choice(self,level_option):
        Select(self.course_level_button).select_by_visible_text(level_option)
        self.hours_weekly_slider = WebDriverWait(self._driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.HOURS_SLIDER)))


    def set_hours_weekly_slider(self,hours_weekly):
        self._driver.execute_script("arguments[0].scrollIntoView(true);", self.hours_weekly_slider)
        current_value = int(self.hours_weekly_slider.get_attribute("aria-valuenow"))
        offset=(hours_weekly-current_value)
        actions =ActionChains(self._driver)
        actions.click_and_hold(self.hours_weekly_slider).move_by_offset(offset*6, 0)
        actions.release()
        actions.perform()



    def click_on_create_button(self):
        self.create_button=WebDriverWait(self._driver,15).until(EC.visibility_of_element_located((By.XPATH, self.CREATE_BUTTON))).click()
    def set_goal_in_web(self,goal_name,chosen_skills,courses_levels,hours_weekly):
        self.init()
        self.click_on_add_a_goal_button(goal_name)
        self.click_on_goal_name_button()
        self.click_on_continue_button()
        self.click_on_add_additional_skills_button()
        for skill, level in zip(chosen_skills, courses_levels):
            self.click_on_skills_checkbox(skill)
            self.set_course_level_to_your_choice(level)
        self.set_hours_weekly_slider(hours_weekly)
        self.click_on_create_button()

    def extract_goal_skills_level(self,goal_name):
        try:
            self.goal_name_in_my_goals=WebDriverWait(self._driver,5).until(EC.visibility_of_element_located((By.XPATH, f'//p[contains(text(),"{goal_name}")]')))
        except TimeoutException:

            self.goal_name_in_my_goals= f"Goal name '{goal_name}' was not found on the page."

        progress_element=self._driver.find_elements(by=By.XPATH, value=f'//p[contains(text(),"{goal_name}")]/ancestor::button/following-sibling::div[3]//p/ancestor::*[3]/div[2]/div[2]')
        self.matching_level_names = []
        percent_to_levels ={value: key for key, value in self.info_api["levels_dict"].items()}
        for element in progress_element:
            left_property = self._driver.execute_script("return window.getComputedStyle(arguments[0],null).getPropertyValue('left');",element)
            percentage_match = re.search(r'calc\((\d+)%', left_property)
            if percentage_match:
                progress_percentage = percentage_match.group(1)
                percentage_int = int(progress_percentage)
                level_name = percent_to_levels.get(percentage_int)
                if level_name:
                    self.matching_level_names.append(level_name)
        try:
            self.skills_elements = WebDriverWait(self._driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, f'//p[contains(text(),"{goal_name}")]/ancestor::button/following-sibling::div[3]/div/div/div/div/div/p')))
            self.skills_names=[self._driver.execute_script('return arguments[0].textContent', elem) for elem in self.skills_elements]
        except TimeoutException:
            self.skills_names= f"skills not found on the page."

    def sort_skills_and_levels(self,skills, levels):
        if len(skills) != len(levels):
            raise ValueError("The number of skills must match the number of levels.")
        paired_skills_levels = list(zip(skills, levels))
        paired_skills_levels.sort(key=lambda x: x[0])
        sorted_skills, sorted_levels = zip(*paired_skills_levels)
        return list(sorted_skills), list(sorted_levels)

    def delete_goals(self,goal_name):
        self.locate_edit_goal_button(goal_name)
        self.click_on_edit_goal_button()
        self.click_on_delete_goal_button()
        self.click_on_footer_delete_button()
