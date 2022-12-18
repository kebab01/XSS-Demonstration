import psycopg2
from random import randint
from flask import escape

conn=None
def connect():
    global conn
    try:
        conn = psycopg2.connect(
            host="db",
            database="postgres",
            user="postgres",
            password="postgres")
    except psycopg2.Error as err:
        print(err)

def is_valid_user(username, password):
    connect()
    cursor=conn.cursor()
    cursor.execute("select * from users where username=(%s)", (username,))
    user=cursor.fetchone()
    
    try:
        if password==user[1]:
            return True
        else:
            return False
    except:
        return False

def create_user(username, password):
    
    rand_num=randint(1,11)
    avatar=f'avatar_id{rand_num}.png'
    connect()
    cursor=conn.cursor()
    cursor.execute("insert into users (username, password, avatar) values (%s, %s, %s)", (username, password, avatar))
    conn.commit()

def getPosts():
    connect()
    cursor=conn.cursor()
    cursor.execute("select title, author, content from posts")
    results=cursor.fetchall()
    posts=[{
        "title":i[0],
        "user":i[1],
        "content":i[2]
    } for i in results] 
    return posts

def addPost(user, title, content):
    connect()
    cursor=conn.cursor()
    cursor.execute("insert into posts (title, author, content) values (%s, %s, %s)", (title, user, content))
    conn.commit()

def getAvatar(user):
    connect()
    cursor=conn.cursor()
    cursor.execute("select avatar from users where username=(%s)", (user,))
    avatar=cursor.fetchone()

    if avatar != None:
        return avatar[0]

def sanitize_post(post):
    
    post['content']=escape(post['content'])
    post['title']=escape(post['title'])

    return post

def valid_user(user):
    connect()
    cursor=conn.cursor()
    cursor.execute("select * from users where username=(%s)", (user,))
    user=cursor.fetchone()

    if user ==None:
        return False

    return True