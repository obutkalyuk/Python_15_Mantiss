import mysql.connector
from model.group import Group
from model.contact import Contact

class DbFixture:
    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = mysql.connector.connect(host=host, database=name, user=user, password=password)
        self.connection.autocommit = True


    def get_group_list(self):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select group_id, group_name, group_header, group_footer from group_list")
            for row in cursor:
                (id, name, header, footer) = row
                list.append( Group(id=str(id), name=name, header=header, footer=footer))

        finally:
            cursor.close()
        return list


    def get_contact_list(self):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, firstname, lastname, address, home, mobile, work, email, email2, email3 FROM addressbook WHERE deprecated ='0000-00-00 00:00:00'")
            for row in cursor:
                (id, firstName, lastName, address, homePhone, mobilePhone, workPhone, email1, email2, email3) = row
                Contact()
                list.append( Contact(id=str(id), firstName=firstName, lastName=lastName, address=address,
                                     homePhone=homePhone, mobilePhone=mobilePhone, workPhone=workPhone,
                                     email1=email1, email2=email2, email3=email3))

        finally:
            cursor.close()
        return list

    def destroy(self):
        self.connection.close()