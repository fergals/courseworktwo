import datetime
from flask.ext.login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('secondcoursework.db')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    adminauth = BooleanField(default=False)
	  
    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)
        
    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            cls.create(
                username=username,
                email=email,
                password=password,
                adminauthn=admin)
        except IntegrityError:
            raise ValueError("User already exists")
            

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()