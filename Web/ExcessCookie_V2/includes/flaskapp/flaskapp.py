from flask import Flask, render_template, url_for, request, redirect, send_from_directory, make_response
from flask_pymongo import PyMongo
from flask_recaptcha import ReCaptcha
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import jwt
import bcrypt
import urllib
import os
from bson.objectid import ObjectId
from decouple import config
from datetime import datetime


DB_URL = config('DB_URL')
UPLOAD_PATH = config('UPLOAD_PATH')
SECRET_KEY = config('SECRET_KEY')

app = Flask(__name__)
app.secret_key = SECRET_KEY

# -----------------------------GOOGLE RECAPTCHA CONFIG------------------

app.config['RECAPTCHA_SITE_KEY'] = config('RECAPTCHA_SITE_KEY')
app.config['RECAPTCHA_SECRET_KEY'] = config('RECAPTCHA_SECRET_KEY')

recaptcha = ReCaptcha(app)

# -------------------------------DATABASE---------------------------------

mongodb_client = PyMongo(app, uri=DB_URL)
db = mongodb_client.db

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'svg'])
app.config['UPLOAD_PATH'] = UPLOAD_PATH
app.config['MAX_CONTENT_LENGTH'] = 1* 1000 * 1000


# --------------------------JWT SESSION MANAGMENT--------------------------


def encodeJWT(userName):
    encoded_token = jwt.encode(
        {'uname': userName}, SECRET_KEY, algorithm='HS256')
    return encoded_token


def decodeJWT(jwtToken):
    try:
        decoded_Payload = jwt.decode(
            jwtToken, SECRET_KEY, algorithms=['HS256'])
        uName = decoded_Payload['uname']
        if uName != None:
            return str(uName).strip()
        else:
            return None
    except Exception as e:
        return None

# -----------------------------ROUTING FUNCTIONS-----------------------------


@app.route("/", methods=['GET', 'POST'])
def login():
    if request.cookies.get('auth'):
        return redirect('/home')

    if request.method == 'POST':
        try:
            username = str(request.form['username']).strip()
            login_user = db.users.find_one(
                {'username': username})
            if login_user:

                if check_password_hash(login_user['password'], request.form['password']):
                    response = make_response(redirect('/home'))
                    response.set_cookie('auth', encodeJWT(
                        username), httponly = True)
                    return response

            return render_template('login.html', data="Invalid Credentials")

        except Exception as e:
            print(e)
            return redirect('/')

    return render_template('login.html', data='')


@app.route("/home")
def index():
    auth_cookie = request.cookies.get('auth')
    try:
        if decodeJWT(auth_cookie):
            data = db.users.find_one({'username': decodeJWT(auth_cookie)})
            return render_template('index.html', data=data)
        else:
            response = make_response(redirect('/'))
            response.delete_cookie('auth')
            return response

    except Exception as e:
        print(e)
        return redirect('/')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = str(request.form['username']).strip()
            existing_user = db.users.find_one(
                {'username': username})

            if existing_user is None:
                if username == 'defaultProfile':
                    return render_template('login.html', data="Choose a different username.")

                hashpass = generate_password_hash(
                    str(request.form['password']), "sha256")
                db.users.insert_one(
                    {
                        'fullname': str(request.form['fullname']),
                        'username': username,
                        'password': hashpass,
                        'email': 'Not Added',
                        'gender': 'Not Added',
                        'about': 'Not Added',
                        'profilePic': 'defaultProfile.jpg',
                        'posts': [],
                    })
                response = make_response(redirect('/home'))
                response.set_cookie('auth', encodeJWT(
                    username), httponly = True)
                return response
            else:
                return render_template('login.html', data="Username already exist.")
        except Exception as e:
            print(e)
            return redirect('/')

    return render_template('register.html')


@app.route("/compose", methods=['GET', 'POST'])
def compose():
    auth_cookie = request.cookies.get('auth')
    try:
        username = decodeJWT(auth_cookie)
        ADMIN_USERNAME = config('ADMIN_USERNAME')
        if username:
            if request.method == 'POST' and username != ADMIN_USERNAME:
                postTitle = str(request.form['postTitle'])
                postContent = str(request.form['postBody'])
                db.users.update_one({'username': decodeJWT(auth_cookie)}, {
                                    '$push': {'posts': [postTitle, postContent]}})
                return redirect('/home')
            return render_template('compose.html')
        else:
            return redirect('/')

    except Exception as e:
        print(e)
        return redirect('/')


@app.route("/report", methods=['GET', 'POST'])
def report():
    auth_cookie = request.cookies.get('auth')
    try:
        if decodeJWT(auth_cookie):
            if request.method == 'POST':
                if recaptcha.verify():
                    uuid = str(request.form['uuid'])
                    complaint = str(request.form['complaint'])
                    userExist = db.users.find_one({'_id': ObjectId(uuid)})
                    if userExist != None and userExist != []:
                        if(int(db.reports.count_documents({'reporter': str(userExist['_id']), "checked": False})) <= 5):
                            db.reports.insert_one(
                                {
                                    'reporter': str(db.users.find_one({'username': decodeJWT(auth_cookie)})['_id']),
                                    'reported': str(userExist['_id']),
                                    'complaint': complaint,
                                    'checked': False,
                                    'reportedAt': datetime.now()
                                })
                            return render_template('report.html', data="Noted, by Admin.")
                        else:
                            return render_template('report.html', data="You already made many reports, please wait for some time.")

                    else:
                        return render_template('report.html', data="No User is found.")
                else:
                    return render_template('report.html', data="Invalid Captcha.")

            return render_template('report.html', data='')
        else:
            return redirect('/')

    except Exception as e:
        print(e)
        return redirect('/')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploads(filename):
    filename = urllib.parse.unquote(filename)
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route("/uploadProfile", methods=["POST"])
def uploadProfile():
    try:
        auth_cookie = request.cookies.get('auth')
        username = str(decodeJWT(auth_cookie))
        if username == 'None':
            return "Please login first."
        file = request.files['profilePic']
        if 'profilePic' in request.files and allowed_file(file.filename):
            fileExtension = file.filename.rsplit('.', 1)[1].lower()
            fileName = secure_filename(username) + '.' + fileExtension
            file.save(os.path.join(app.config['UPLOAD_PATH'], fileName))
            db.users.update_one({'username': decodeJWT(auth_cookie)}, {
                '$set': {
                    'profilePic': fileName
                }
            })
        else:
            return 'File type not accepted.'

        return redirect('/')
    except Exception as e:
        print(e)
        return redirect('/')

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    auth_cookie = request.cookies.get('auth')
    try:
        if decodeJWT(auth_cookie):
            if request.method == 'POST':
                changedFullname = str(request.form['fullname'])
                changedEmail = str(request.form['email'])
                changedGender = str(request.form['gender'])
                changedAbout = str(request.form['about'])
                db.users.update_one({'username': decodeJWT(auth_cookie)}, {
                    '$set': {
                        'fullname': changedFullname,
                        'email': changedEmail,
                        'gender': changedGender,
                        'about': changedAbout,
                    }
                })
                return redirect('/home')

            data = db.users.find_one({'username': decodeJWT(auth_cookie)})
            return render_template('profile.html', data=data)

        else:
            return redirect('/')

    except Exception as e:
        print(e)
        return redirect('/')


@app.route('/user/<uuid>')
def showProfile(uuid):
    auth_cookie = request.cookies.get('auth')
    try:
        if decodeJWT(auth_cookie):
            if uuid == '61c8b1f9beceeaa92ab06c00':
                data = {
                    "_id": ObjectId("61c8b1f9beceeaa92ab06c00"),
                    "fullname": "Anonymous",
                    "email": "anonymous@pctf.in",
                    "gender": "Not interested to say.",
                    "about": "I myself anonymous, how can i say about me.",
                    "profilePic": "defaultProfile.jpg",
                    "posts": [["Nothing to say much, just one thing", "The image with which you see a person from outside won't be the same as from inside."]]
                }
                return render_template('show.html', data=data)
            else:
                data = db.users.find_one({'_id': ObjectId(uuid)})
                if data != None and data != []:
                    return render_template('show.html', data=data)
                else:
                    return render_template('show.html', data=None)
        else:
            return redirect('/')

    except Exception as e:
        print(e)
        return redirect('/')


@app.route("/search", methods=['GET', 'POST'])
def search():
    auth_cookie = request.cookies.get('auth')
    try:
        if decodeJWT(auth_cookie):
            if request.method == 'POST':
                searchedUUID = str(request.form['searchUUID'])
                return redirect('/user/'+searchedUUID)
            else:
                return render_template('search.html')

        else:
            return redirect('/')

    except Exception as e:
        print(e)
        return redirect('/')


@app.route("/logout")
def logout():
    response = make_response(redirect('/'))
    response.delete_cookie('auth')
    return response


@app.route("/status")
def status():
    POST_CONTENT = config('POST_CONTENT')
    ADMIN_ID = config('ADMIN_UUID')
    ADMIN_USERNAME = config('ADMIN_USERNAME')
    admin_account = db.users.find_one({'username': ADMIN_USERNAME})
    if admin_account != None and admin_account != []:
        if admin_account['_id'] == ObjectId(ADMIN_ID) and admin_account['username'] == ADMIN_USERNAME and admin_account['posts'][0][1] == POST_CONTENT:
            return "OK"
        else:
            return "Admin account is not set properly.", 500
    else:
        return "Admin account not found.", 500

@app.errorhandler(413)
def page_not_found(e):
    return render_template('errors.html', data="File size should not exceed 1MB.")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
