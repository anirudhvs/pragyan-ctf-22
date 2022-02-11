from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from decouple import config
from bson.objectid import ObjectId


DB_URL = config('DB_URL')
SECRET_KEY = config('SECRET_KEY')
ADMIN_USERNAME = config('ADMIN_USERNAME')
ADMIN_FULLNAME = config('ADMIN_FULLNAME')
ADMIN_PASSWORD = config('ADMIN_PASSWORD')
POST_TITLE = config('POST_TITLE')
POST_CONTENT = config('POST_CONTENT')
ADMIN_ID = config('ADMIN_UUID')

mongodb_client = MongoClient(DB_URL)
db = mongodb_client['SVG_XSS']


hashpass = generate_password_hash(ADMIN_PASSWORD, "sha256")

db.users.update_one(
    {'fullname': ADMIN_FULLNAME}, 
    {
        '$set':
        {
            '_id' : ObjectId(ADMIN_ID),
            'fullname': ADMIN_FULLNAME, 
            'username' : ADMIN_USERNAME, 
            'password' : hashpass,
            'email' : 'adminSecuremail@pctf.in',
            'gender' : 'MALE',
            'about' : 'Nothing to say much.',
            'profilePic' : 'defaultProfile.jpg',
            'posts' : [[POST_TITLE, POST_CONTENT]]
        }
    },
    upsert=True
)

print('Seeding Completed.')