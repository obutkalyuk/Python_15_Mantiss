from selenium import webdriver
from fixture.session import SessionHelper
from fixture.project import ProjectHelper
from selenium.webdriver.support.wait import WebDriverWait


class Application:
    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()

        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "Ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("incorrect browser %s" % browser)

        self.wait  = WebDriverWait(self.wd, 10)
        self.wd.implicitly_wait(5)
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.base_url = base_url

    def destroy(self):
        self.wd.quit()


    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_home_page(self):
        wd = self.wd
        wd.maximize_window()
        wd.get(self.base_url)

    def type_text(self, attribute,  text):
        wd = self.wd
        if text is not None:
            wd.find_element_by_name(attribute).click()
            wd.find_element_by_name(attribute).clear()
            wd.find_element_by_name(attribute).send_keys(text)

    def go_to_control_page(self):
        wd = self.wd
        control_link = wd.find_element_by_css_selector("a[href$='manage_overview_page.php']")
        control_link.click()
