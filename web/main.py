from flask import Flask, make_response, redirect, url_for, render_template, request, session, send_file, escape

from functions import addPost, is_valid_user, create_user, getPosts, sanitize_post, getAvatar, valid_user

from flask.sessions import SecureCookieSessionInterface

app=Flask(__name__)
app.secret_key="MY_SUPER_SECRET_KEY"

session_serializer = SecureCookieSessionInterface().get_signing_serializer(app)

SANITIZE_ENABLE=False

print('starting')
@app.route("/")
def root():
    response=make_response()
    response.location=url_for('login')
    response.status=302
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        if 'login' in request.form:
            username=request.form['uname']
            password=request.form['passwd']
            if is_valid_user(username=username,password=password):

                # Set session cookie without httpOnly flag
                r=make_response()
                r.location=url_for('forum')
                r.status=302

                session_cookie={
                    'user':username
                }
                cookie=session_serializer.dumps(session_cookie)
                r.set_cookie('session', cookie)
                return r
            return render_template("login.html", failed=True)
        return redirect(url_for("sign_up"))
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    print('in sign up')
    if request.method=="POST":
        if request.form['passwd']!= request.form['conf_passwd']:
            print("passwords do not match")
            user=request.form['uname']
            return render_template('signup.html', pass_match=False, user=user)
        else:
            create_user(username=request.form['uname'], password=request.form['passwd'])
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route("/forum", methods=["GET"])
def forum():
    posts=getPosts()
    try:
        user=session['user']
        if not valid_user(user):
            raise Exception ("Invalid user")

        avatar=getAvatar(user)
        search_param=request.args.get('search')

        if SANITIZE_ENABLE:
            posts=[sanitize_post(i) for i in posts]
            search_param=escape(search_param)

        if search_param != None and search_param != '':    
            posts=list(filter(lambda x: search_param.lower() in x['title'].lower(), posts))
        else:
            search_param=None
            
        return render_template('forum.html', user=user, posts=posts, num_of_posts=len(posts), avatar=avatar, search_param=search_param)
    except Exception:
        return redirect(url_for('login'))

@app.route("/profile", methods=["GET"])
def profile():
    avatar=getAvatar(session['user'])
    return render_template('profile.html', user=session['user'], avatar=avatar)

@app.route("/post", methods=["POST"])
def add_post():
    title=request.form['title']
    content=request.form['content']
    addPost(user=session['user'],content=content, title=title)
    return redirect(url_for('forum'))

@app.route("/image/<img>", methods=["GET"])
def get_image(img):
    return send_file(f"./assets/{img}")

@app.route('/signout', methods=['GET'])
def sign_out():
    return redirect(url_for('login'))

if __name__=="__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")
