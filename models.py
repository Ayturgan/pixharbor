from peewee import *
import datetime
from flask_login import UserMixin


db = SqliteDatabase('database.db')

db.connect()

class BaseModel(Model):
    class Meta:
        database = db

class Users(UserMixin, BaseModel):
    username = CharField(max_length=255, null=False, unique=True)
    email = CharField(max_length=255, null=False, unique=True)
    age = IntegerField(null=True)
    location = CharField(max_length=255, null=True)
    about_me = TextField(null=True)
    specialization = CharField(max_length=255, null=True)
    full_name = CharField(max_length=255, null=True)
    password = CharField(max_length=255, null=False)
    image = CharField(max_length=255, null=True, default='media/avatars/default_avatar.png')

    def __repr__(self):
        return self.email

class Posts(BaseModel):
    author = ForeignKeyField(Users, on_delete='CASCADE')
    title = CharField(max_length=255, null=False)
    content = TextField(null=True)
    created_date = DateTimeField(default=datetime.datetime.now)
    image = CharField(max_length=255, null=False)
    


    def __repr__(self):
        return self.title
    
class Comments(BaseModel):
    post = ForeignKeyField(Posts, on_delete='CASCADE')
    author = ForeignKeyField(Users, on_delete='CASCADE')
    content = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)

    def __repr__(self):
        return self.content



db.create_tables([Users, Posts, Comments])






