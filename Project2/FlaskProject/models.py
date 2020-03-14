from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from FlaskProject import mysql, bcrypt, login_manager
from flask_login import UserMixin, current_user
from flask import current_app

@login_manager.user_loader
def loader_user(user_id):
    cur = mysql.connection.cursor()
    count = cur.execute(f"SELECT * FROM userInfo WHERE id = '{user_id}'")
    result= cur.fetchall()
    mysql.connection.commit()
    cur.close()
    if count > 0:
        user = User(result[0][1], result[0][2], result[0][3], result[0][4])
        return user
    else:
        return None


class User(UserMixin):
    def __init__(self, username, passwd, email='', image_file='default-avatar.jpg'):
        self.__username = username
        self.__passwd = passwd
        self.__email = email 
        self.__image_file=image_file
    def get_name(self):
        return self.__username
    def get_email(self):
        return self.__email
    def get_image(self):
        return self.__image_file
    def createUser(self):
        cur = mysql.connection.cursor()
        count = cur.execute(f"SELECT * FROM userInfo WHERE username = '{self.__username}'")
        if count == 0:
            hashed_pw = bcrypt.generate_password_hash(self.__passwd).decode('utf-8')
            cur.execute("INSERT INTO userInfo(username, passwd, email) VALUES(%s,%s,%s)",(self.__username, hashed_pw, self.__email))
            mysql.connection.commit()
            cur.close()
            return True
        else:
            cur.close()
            return False
    
    def checkUser(self):
        cur = mysql.connection.cursor()
        count = cur.execute(f"SELECT passwd FROM userInfo WHERE username = '{self.__username}'")
        result = cur.fetchall()
        mysql.connection.commit()
        cur.close() 
        if count > 0:
            if bcrypt.check_password_hash(result[0][0], self.__passwd)==True:
                return 1
            else:
                return 0
        else:
             return -1 

    def updateUser(self, username, email, picture):
        cur = mysql.connection.cursor()
        countUser = cur.execute(f"SELECT * FROM userInfo WHERE username= '{username}'")
        name = current_user.get_name()
        if countUser != 0 and username != name:
            return False
        else:
            self.__username = username
            self.__email = email
            self.__image_file = picture
            cur.execute(f"UPDATE userInfo SET username='{username}', email='{email}', picture='{picture}' WHERE username='{name}'")
            mysql.connection.commit()
            cur.close()
            return True

    @staticmethod
    def reset_user_password(username, Npasswd):
        cur = mysql.connection.cursor()
        hash_passwd = bcrypt.generate_password_hash(Npasswd).decode('utf-8')
        cur.execute(f"UPDATE userInfo SET passwd='{hash_passwd}' WHERE username='{username}'")
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def get_token(username):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in = 600)
        return s.dumps({'username': username}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            return s.loads(token)['username']
        except:
            return None


    @staticmethod
    def check_email(email):
        cur = mysql.connection.cursor()
        count = cur.execute(f"SELECT * FROM userInfo WHERE email='{email}'") 
        result= cur.fetchall()
        mysql.connection.commit()
        cur.close()
        if count > 0:
            return result[0][1]
        else:
            return None

    def get_id(self):
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT id FROM userInfo WHERE username = '{self.__username}'")
        result= cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return result[0][0]

class Post:
    @classmethod
    def createPost(cls, title, content):
        cur=mysql.connection.cursor()
        timestampStr = datetime.now().strftime("%d-%b-%Y (%H:%M)")
        cur.execute("INSERT INTO posts(title, content, date_posted, author_id) VALUES(%s,%s,%s,%s)",(title, content, timestampStr, current_user.get_id()))
        mysql.connection.commit()
        cur.close()

    @classmethod
    def updatePost(cls, title, content, post_id):
        cur=mysql.connection.cursor()
        timestampStr = datetime.now().strftime("%d-%b-%Y (%H:%M)")
        cur.execute(f'''UPDATE posts 
                        SET title = '{title}', content = '{content}', date_posted= '{timestampStr}' 
                        WHERE post_id = {post_id}''')
        mysql.connection.commit()
        cur.close()

    @classmethod
    def detelePost(cls, post_id):
        cur=mysql.connection.cursor()
        cur.execute(f'''DELETE FROM posts  
                        WHERE post_id = {post_id}''')
        mysql.connection.commit()
        cur.close()

    @classmethod
    def getPosts(cls):
        cur=mysql.connection.cursor()
        count = cur.execute('''SELECT post_id, title, content, date_posted, username, author_id
                               FROM posts p
                               JOIN userInfo u
                               ON p.author_id = u.id''')
        posts= cur.fetchall()
        mysql.connection.commit()
        cur.close()
        if count != 0:
            return posts
        else:
            return None

    @classmethod
    def get_post(cls, post_id):
        cur = mysql.connection.cursor()
        cur.execute(f'''SELECT post_id, title, content, date_posted, username, author_id 
                        FROM posts p
                        JOIN userInfo u
                        ON p.author_id = u.id 
                        WHERE post_id = {post_id}''')
        result= cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return result[0]

    @classmethod
    def get_user_posts(cls, author_id):
        cur = mysql.connection.cursor()
        cur.execute(f'''SELECT post_id, title, content, date_posted, username, author_id
                        FROM posts
                        JOIN userInfo
                        ON posts.author_id = userInfo.id  
                        WHERE author_id={author_id}''')
        posts= cur.fetchall()
        return posts
        
