import os
import json
file = open('C:\\Users\\Le Nhat\\VSC project\\Project2\\FlaskProject\\config.json', 'r')
dic = json.load(file)
class Config:
    SECRET_KEY = dic.get('SECRET_KEY')
    MYSQL_HOST = dic.get('MYSQL_HOST')
    MYSQL_USER = dic.get('MYSQL_USER')
    MYSQL_PASSWORD  =dic.get('MYSQL_PASSWORD')
    MYSQL_DB = dic.get('MYSQL_DB')
    MYSQL_PORT = dic.get('MYSQL_PORT')

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS= True
    MAIL_USERNAME = dic.get('MAIL_USERNAME')
    MAIL_PASSWORD = dic.get('MAIL_PASSWORD')