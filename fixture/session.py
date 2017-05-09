class SessionHelper:
    def __init__(self, app):
        self.app = app

    def login(self, user, password):
        wd = self.app.wd
        self.app.open_home_page()
        self.app.type_text("user", user)
        self.app.type_text("pass", password)
        wd.find_element_by_css_selector("input[value='Login']").click()

    def ensure_login(self, user, password):
        wd = self.app.wd
        if self.is_logged_in():
            if self.is_logged_in_as(user):
                return
            else:
                self.logout()
        self.login(user,password)

    def logout(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Logout").click()

    def ensure_logout(self):
        wd = self.app.wd
        if self.is_logged_in():
            self.logout()

    def is_logged_in(self):
        wd = self.app.wd
        return len(wd.find_elements_by_link_text("Logout"))> 0

    def is_logged_in_as(self, user):
        wd = self.app.wd
        return self.get_logged_user() == user

    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element_by_xpath("//form[@name='logout']/b").text[1:-1]

