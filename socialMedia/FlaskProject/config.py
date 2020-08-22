import os
import json

file = open('config.json', 'r')
dic = json.load(file)
class Config:
    SECRET_KEY = dic.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = dic.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS= True
    MAIL_USERNAME = dic.get('MAIL_USERNAME')
    MAIL_PASSWORD = dic.get('MAIL_PASSWORD')
