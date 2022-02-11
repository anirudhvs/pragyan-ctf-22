from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config
from datetime import datetime

DB_URL = config('DB_URL')
DOMAIN_URL = config('DOMAIN_URL')
ADMIN_COOKIE = config('ADMIN_COOKIE')
TIMEOUT_FOR_USER = config('TIMEOUT_FOR_USER', cast=int)
JOB_WAIT_TIME = config('JOB_WAIT_TIME', cast=int)

# print(DB_URL, DOMAIN_URL, ADMIN_COOKIE)
client = MongoClient(DB_URL)

db=client.SVG_XSS

while True:
    reportedUsers = db.reports.find({"checked":False})
    reported_count = 0
    for user in reportedUsers:
        print(str(datetime.now())+" -> User: "+str(user))
        reported_count += 1
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option('prefs', {
            'credentials_enable_service': False,
            'download_restrictions': 3,
            'profile': {
                'password_manager_enabled': False
            }
        })
        
        browser = webdriver.Chrome(options=chrome_options)
        try:
            browser.get(DOMAIN_URL)
            cookie_dict = {'name' : 'auth', 'value': ADMIN_COOKIE}
            browser.add_cookie(cookie_dict)
            user_id = user.get('reported')
            browser.get(DOMAIN_URL+'/user/'+str(user_id))
            image = browser.find_element(By.TAG_NAME, 'img').get_attribute("src")
            browser.get(str(image))
            sleep(TIMEOUT_FOR_USER)
            # print(traceback.format_exc())
            browser.quit()
        except Exception as e:
            print("Exception is: ", e)
        finally:
            db.reports.update_one({'_id' : ObjectId(user.get('_id'))}, {'$set' : {'checked': True}})
    if reported_count == 0:
        print(str(datetime.now())+'-> No new reports')
        sleep(JOB_WAIT_TIME)
