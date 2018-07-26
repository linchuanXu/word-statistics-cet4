# coding = utf-8
# description
# expand exsited database, add some nessary column, and reserve some columns
# 使用 peewee 库操作 sqlite3
# 建立两个 table: word-book
# 以下为 newword 的原因是由于之前创建过一次，但需要扩展字段
# 所有迁移了数据，重新建了表

from settings import DATABASE
from peewee import *

db = SqliteDatabase(DATABASE) #创建数据库类

class NewBook(model):
    name = CharField()
    total = IntegerField() #总词汇
    is_analyzed = BooleanField()
    # reserved columns
    # 保留字段，便于之后扩展
    re1 = CharField(default='')
    re2 = CharField(default='')
    re3 = IntegerField(default=0)
    re4 = IntegerField(default=0)

    class Meta:
        database = db

class NewWord(Model):
    # foreignkey , which books the word collect from
    # book = ForeignKeyField(Book)
    # 单词名
    name = CharField()
    # 解释
    explanation = TextField(default='')
    # 词频
    frequency = IntegerField(default=0)
    # 是否有效
    is_valid = BooleanField(default=True)
    # 音标
    phonogram = CharField(default='')
    # reserved columns
    # 保留字段，便于之后扩展
    re1 = CharField(default='')
    re2 = CharField(default='')
    re3 = IntegerField(default=0)
    re4 = IntegerField(default=0)

    class Meta:
        database = db
