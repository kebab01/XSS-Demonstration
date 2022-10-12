import psycopg2

USER="tom"
PASS="asdf"

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
    
    connect()
    cursor=conn.cursor()
    cursor.execute("insert into users (username, password) values (%s, %s)", (username, password))
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
        
def sanitize_post(post):
    
    content=post['content']
    title=post['title']

    content=content.replace("<","")
    content=content.replace(">","")
    
    title=title.replace("<","")
    title=title.replace(">","")

    post['content']=content
    post['title']=title

    print(post)
    return post