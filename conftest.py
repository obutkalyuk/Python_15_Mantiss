import pytest
from fixture.application import Application
from fixture.db import DbFixture
from fixture.orm import ORMFixture
import jsonpickle
import json
import os.path
import importlib


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
def check_ui(request):
    return request.config.getoption("--check-ui")

@pytest.fixture
def app(request):
    global fixture

    browser = request.config.getoption("--browser")
    web_config= load_config(request.config.getoption("--target"))['web']

    if (fixture is None) or (not fixture.is_valid()):
        fixture = Application(browser = browser, base_url = web_config["baseUrl"])
    fixture.session.ensure_login(user=web_config["user"], password=web_config["password"])

    return fixture

# via SQL
# @pytest.fixture(scope = 'session')
# def db(request):
#     db_config= load_config(request.config.getoption("--target"))['db']
#
#     dbfixture = DbFixture(host=db_config['host'], name = db_config['name'], user = db_config['user'], password = db_config['password'])
#     def fin():
#         dbfixture.destroy()
#     request.addfinalizer(fin)
#     return dbfixture

#  via ORM
@pytest.fixture(scope = 'session')
def db(request):
    db_config= load_config(request.config.getoption("--target"))['db']

    dbfixture = ORMFixture(host=db_config['host'], name = db_config['name'], user = db_config['user'], password = db_config['password'])


    return dbfixture

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
    parser.addoption("--check-ui", action ="store_true")

def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids= [str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids= [str(x) for x in testdata])


def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata

def load_from_json(file):
    full_json_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)
    with open(full_json_name) as f:
         return jsonpickle.decode(f.read())
    pass




