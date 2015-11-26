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
	
	def get_posts(self):
		return Post.select().where(Post.user == self)
	
	def get_all(self):
		return Post.select().where(
			(Post.user == self)
			)
        
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
            
class Post(Model):
    timestamp = DateTimeField(default=datetime.datetime.now) #timestamp for new post
    user = ForeignKeyField(
        rel_model=User, #Sql Foreign Key = User
        related_name='posts'
    )
    content = TextField()
	tags = TextField()
    
    class Meta:
        database = DATABASE
        order_by = ('-timestamp',) #newest items appear at top
		
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post], safe=True)
    DATABASE.close()