import datetime
from flask.ext.login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('secondcoursework.db')

class User(UserMixin, Model):
      username = CharField(unique=True)
	  password = Charfield(max_length=50)
	  email = CharField(unique=True)
	  joined = DateTimeField(default=datetime.datetime.now)
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
							password=password
							adminauth=admin)
			except IntegrityError:
				raise ValueError("Uh Oh! User already exists")
		