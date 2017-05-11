import pytest
from fixture.application import Application
import json
import os.path



fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        full_config_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(full_config_name) as config_file:
            target = json.load(config_file)
    return target

@pytest.fixture
def app(request):
    global fixture

    browser = request.config.getoption("--browser")
    webadmin_config= load_config(request.config.getoption("--target"))['webadmin']
    web_config= load_config(request.config.getoption("--target"))['web']

    if (fixture is None) or (not fixture.is_valid()):
        fixture = Application(browser = browser, base_url = web_config["baseUrl"])
    fixture.session.ensure_login(user=webadmin_config["user"], password=webadmin_config["password"])
    # fixture.session.go_to_control_page()
    return fixture


@pytest.fixture(scope = 'session', autouse = True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

def pytest_addoption(parser):
    parser.addoption("--browser", action ="store", default = "firefox")
    parser.addoption("--target", action ="store", default = "target.json")





