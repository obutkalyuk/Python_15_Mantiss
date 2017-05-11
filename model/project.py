from sys import maxsize
from fixture.string_helper import *

class Project:
    def __init__(self, id = None,  name=None, status=None, inherit_global=None, view_state = None, description=None):
        self.id = id
        self.name = name
        self.status = status
        self.inherit_global = inherit_global
        self.view_state = view_state
        self.description = description


    def random(self, id = None,  name=None, status=None, inherit_global=None, view_state = None, description=None):
        self.id = id
        self.name = random_string("name", 10)
        self.status = self.random_status()
        self.inherit_global = random_bool()
        self.view_state = self.random_view_state()
        self.description = random_string("Description ", 20)
        return self


        return self

    def random_status(self):
        status = ("development", "realize", "statement", "obsolete")
        return random.choice(status)

    def random_view_state(self):
        status = ("public", "private")
        return random.choice(status)

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize

    def __repr__(self):
        return "%s: '%s'" % (self.id, self.name)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name