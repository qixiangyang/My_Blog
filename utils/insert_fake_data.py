"""
Description:
Author:qxy
Date: 2019/10/10 7:03 下午
File: insert_fake_data 
"""

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, TIMESTAMP
from sqlalchemy.orm import sessionmaker
import os
import time



class Config:
    pass

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345678@localhost/wangyuebing'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345678@localhost/blog_data'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

url = config.get(os.getenv('FLASK_ENV') or 'default').SQLALCHEMY_DATABASE_URI

engine = create_engine(url)
Base = declarative_base()


class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(64), unique=True)
    text = Column(String())
    author = Column(String(20))
    category = Column(String(20))
    tags = Column(String(50))
    create_time = Column(TIMESTAMP)
    update_time = Column(TIMESTAMP)
    upload_time = Column(TIMESTAMP)
    other_info = Column(String(100))


class PyNews(Base):
    __tablename__ = 'pynews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(64), unique=True)
    text = Column(String())
    author = Column(String(20))
    category = Column(String(20))
    tags = Column(String(20))
    read_count = Column(Integer)
    pub_time = Column(TIMESTAMP())
    url = Column(String(100))
    other_info = Column(String(100))


Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()


def get_fake_article():
    fake_data_list = []
    fake = Faker(locale='zh_CN')

    for _ in range(20):
        data = dict()
        data['author'] = fake.name()
        data['title'] = fake.sentence()
        data['text'] = fake.paragraph(10)
        data['category'] = fake.word()
        data['tags'] = fake.words(5)
        data['create_time'] = fake.date()
        data['update_time'] = fake.date()
        data['upload_time'] = fake.date()
        data['other_info'] = fake.password(special_chars=False)

        fake_data_list.append(data)

    return fake_data_list


def get_fake_pynews():

    fake_data_list = []
    fake = Faker(locale='zh_CN')

    for _ in range(60):
        data = dict()
        data['author'] = fake.name()
        data['title'] = fake.sentence()
        data['text'] = fake.paragraph(10)
        data['category'] = fake.word()
        data['tags'] = fake.words(5)
        data['pub_time'] = fake.unix_time()
        data['read_count'] = fake.pyint()
        data['other_info'] = fake.password(special_chars=False)
        data['url'] = fake.url()

        fake_data_list.append(data)

    return fake_data_list


def insert_article():
    fake_data_list = get_fake_article()
    sql_obj = []
    for data in fake_data_list:
        print(data)
        article_data_online = Article(title=data['title'], text=data['text'], author=data['author'],
                                      category=data['category'], tags=data['tags'], create_time=data['create_time'],
                                      update_time=data['update_time'], upload_time=data['upload_time'],
                                      other_info=data['other_info'])

        sql_obj.append(article_data_online)

    session.add_all(sql_obj)
    session.commit()
    print("article 数据插入完成")


def insert_pynews():
    fake_data_list = get_fake_pynews()

    sql_obj = []
    for data in fake_data_list:
        print(data)
        article_data_online = PyNews(title=data['title'], text=data['text'], author=data['author'],
                                     category=data['category'], tags=data['tags'], pub_time=data['pub_time'],
                                     read_count=data['read_count'], url=data['url'],
                                     other_info=data['other_info'])

        sql_obj.append(article_data_online)

    session.add_all(sql_obj)
    session.commit()
    print("pynews 数据插入完成")


def update_data():
    data_list = session.query(Article).all()
    for data in data_list:
        print(type(data.pub_time))
        print(time.mktime(data.pub_time.timetuple()))
        data.pub_time = str(int(time.mktime(data.pub_time.timetuple())))
        session.commit()


if __name__ == '__main__':
    insert_article()
    # insert_pynews()
    # insert_article()
    # update_data()