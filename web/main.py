from urllib import response
from flask import Flask, make_response, redirect, url_for, render_template, request, session, Response

from functions import addPost, is_valid_user, create_user, getPosts, sanitize_post

from flask.sessions import SecureCookieSessionInterface

app=Flask(__name__)
app.secret_key="MY_SUPER_SECRET_KEY"

session_serializer = SecureCookieSessionInterface().get_signing_serializer(app)
# session_clone = dict(foo='bar')
# session_cookie_data = session_serializer.dumps(session_clone)


print('starting')
@app.route("/")
def root():
    # return redirect(url_for("login"))
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
            return render_template('signup.html', pass_match=False)
        else:
            create_user(username=request.form['uname'], password=request.form['passwd'])
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route("/forum", methods=["GET"])
def forum():
    posts=getPosts()
    try:
        user=session['user']
        bad_param=request.args.get("bad_param")
        #posts=[sanitize_post(i) for i in posts]
        return render_template('forum.html', user=user, posts=posts, param=bad_param)
    except KeyError:
        return redirect(url_for('login'))

@app.route("/post", methods=["POST"])
def add_post():
    title=request.form['title']
    content=request.form['content']
    addPost(user=session['user'],content=content, title=title)
    return redirect(url_for('forum'))

if __name__=="__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")
