from model.project import Project

class ProjectHelper:
    def __init__(self, app):
        self.app = app

    project_cache = None

    def go_to_project_tab(self):
        wd = self.app.wd
        wd.find_element_by_css_selector("a[href$='manage_proj_page.php']").click()

    def create(self, project):
        wd = self.app.wd
        self.go_to_project_tab()
        wd.find_element_by_css_selector("form[action='manage_proj_create_page.php'] input[type='submit']").click()
        self.set_fields(project)
        wd.find_element_by_css_selector("div.widget-toolbox.padding-8.clearfix > input").click()
        self.project_cache = None

    def select_project_by_index(self, index):
        wd = self.app.wd
        xpath = "(//td/a)[%s]" % str(index+1)
        wd.find_element_by_xpath(xpath).click()

    def select_project_by_id(self, id):
        wd = self.app.wd
        css = "td a[href*='project_id=%s']" % str(id)
        wd.find_element_by_css_selector(css).click()

    def delete_first(self):
        self.delete_by_index(0)

    def delete_by_index(self, index):
        wd = self.app.wd
        self.go_to_project_tab()
        self.select_project_by_index(index)
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        self.project_cache = None

    def delete_by_id(self, id):
        wd = self.app.wd
        self.go_to_project_tab()
        self.select_project_by_id(id)
        delete_button = wd.find_element_by_css_selector("input[value='Delete Project']")
        delete_button.click()
        confirmation_button = wd.find_element_by_css_selector("input[value='Delete Project']")
        confirmation_button.click()
        self.project_cache = None

    # def modify_by_index(self, edition, index):
    #     wd = self.app.wd
    #     self.go_to_project_tab()
    #     self.select_project_by_index(index)
    #     wd.find_element_by_name("edit").click()
    #     self.set_fields(edition)
    #     wd.find_element_by_name("update").click()
    #     self.go_to_project_tab()
    #     self.project_cache = None
    #
    # def modify_by_id(self, edition, id):
    #     wd = self.app.wd
    #     self.go_to_project_tab()
    #     self.select_group_by_id(id)
    #     wd.find_element_by_name("edit").click()
    #     self.set_fields(edition)
    #     wd.find_element_by_name("update").click()
    #     self.go_to_project_tab()
    #     self.project_cache = None
    #
    # def modify_first(self, edition):
    #     self.modify_by_index(edition, 0)

    def count(self):
        wd = self.app.wd
        self.go_to_project_tab()
        return len(wd.find_elements_by_xpath("//td/a[contains(@href, 'project_id')]/../.."))


    # TODO add all fields
    def set_fields(self, project):
        self.app.type_text("name", project.name)
        self.app.type_text("description", project.description)

    def get_project_list(self):
        if self.project_cache is None:
            self.project_cache = []
            wd = self.app.wd
            self.go_to_project_tab()
            for row in wd.find_elements_by_xpath("//td/a[contains(@href, 'project_id')]/../.."):
                id = row.find_element_by_css_selector("a").get_attribute("href").split("=")[1]
                name = row.find_element_by_css_selector("a").text
                status = row.find_element_by_xpath(".//td[2]").text
                view_status = row.find_element_by_xpath(".//td[4]").text
                description = row.find_element_by_xpath(".//td[5]").text
                self.project_cache.append(Project(name=name, id=id, status=status, view_state=view_status, description=description))
        return list(self.project_cache)


