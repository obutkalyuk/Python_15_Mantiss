from pony.orm import *
from datetime import datetime
from model.group import Group
from model.contact import Contact
from pymysql.converters import encoders, decoders, convert_mysql_timestamp



class ORMFixture:

    db = Database()

    class ORM_Group(db.Entity):
        _table_ = 'group_list'
        id = PrimaryKey(int, column='group_id')
        name = Optional(str, column='group_name')
        header = Optional(str, column='group_header')
        footer = Optional(str, column='group_footer')
        contacts = Set(lambda: ORMFixture.ORM_Contact, table="address_in_groups", column="id", reverse="groups", lazy=True)

    class ORM_Contact(db.Entity):
        _table_ ='addressbook'
        id = PrimaryKey(int, column='id')
        firstname = Optional(str, column = 'firstname')
        lastname = Optional(str, column = 'lastname')
        address =  Optional(str, column = 'address')
        homePhone = Optional(str, column = 'home')
        mobilePhone = Optional(str, column = 'mobile')
        workPhone = Optional(str, column = 'work')
        email1 = Optional(str, column = 'email')
        email2 = Optional(str, column = 'email2')
        email3 = Optional(str, column = 'email3')
        deprecated = Optional(str, column = 'deprecated')
        groups = Set(lambda: ORMFixture.ORM_Group,  table="address_in_groups", column="group_id", reverse="contacts", lazy=True)

    def __init__(self, host, name, user, password):
        conv = encoders
        conv.update(decoders)
        conv[datetime] = convert_mysql_timestamp
        self.db.bind('mysql', host=host, database=name, user=user, password=password, conv=conv)
        self.db.generate_mapping()
        sql_debug(True)

    def convert_group_to_model(self, groups):
        def convert(group):
            return Group(id = str(group.id), name = group.name, header = group.header, footer = group.footer)
        return list(map(convert, groups))

    def convert_contacts_to_model(self, contacts):
        def convert(contact):
            return Contact(id=str(contact.id), firstName=contact.firstname, lastName=contact.lastname)
        return list(map(convert, contacts))



    @db_session
    def get_group_list(self):
        return self.convert_group_to_model(select(g for g in ORMFixture.ORM_Group))

    @db_session
    def get_contacts_in_group(self, group):
        orm_group = list(select(g for g in ORMFixture.ORM_Group if g.id==group.id))[0]
        return self.convert_contacts_to_model(orm_group.contacts)

    @db_session
    def get_contacts_not_in_group(self,group):
        orm_group = list(select(g for g in ORMFixture.ORM_Group if g.id == group.id))[0]
        return self.convert_contacts_to_model(
            select(c for c in ORMFixture.ORM_Contact if c.deprecated is None and orm_group not in c.groups))


    @db_session
    def get_contact_list(self):
        return self.convert_contacts_to_model(select(c for c in ORMFixture.ORM_Contact if c.deprecated is None))

    @db_session
    def get_group_with_contacts(self):
        return self.convert_group_to_model(select(g for g in ORMFixture.ORM_Group  if len(g.contacts) !=0))

    @db_session
    def get_contact_without_group(self):
        return self.convert_contacts_to_model(select(c for c in ORMFixture.ORM_Contact  if len(c.groups) ==0))


