from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SkillsPage:
    CHART_TICKS='.recharts-text.recharts-polar-angle-axis-tick-value tspan'
    MY_SKILLS='//div[@class="css-15p1e5z"]//p'

    def __init__(self,driver):
        self._driver =driver
        self.chart_ticks=WebDriverWait(self._driver,30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,self.CHART_TICKS)))
        self.my_skills=self._driver.find_elements(By.XPATH,self.MY_SKILLS)
        self.all_chart_ticks=[]
        self.all_my_skills=[]

    def get_chart_ticks(self):
        for tick in self.chart_ticks:
            self._driver.execute_script("return arguments[0].textContent", tick)
            self.all_chart_ticks.append(tick.text)

    def get_my_skills(self):
        for skill in self.my_skills:
            self.all_my_skills.append(skill.text)