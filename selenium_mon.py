# utilize the same logger function using library? or function
#


from selenium import webdriver
import chromedriver_binary
import time
import requests


##### get user / pass #####

f = open('D:/monitoring/test/user_pass', "r")
u = f.read().splitlines()
myuser = u[0]
mypass = u[1]
f.close()

###########################

driver = webdriver.Chrome()
driver.get("http://helpdesk.corp.dipostar.com/redmine/login/")

id = driver.find_element_by_id("username")
id.send_keys(myuser)

password = driver.find_element_by_id("password")
password.send_keys(mypass)

time.sleep(2)

login_button = driver.find_element_by_name("login")
login_button.click()

# share cookie from selenium to requests
session = requests.session()
for cookie in driver.get_cookies():
    session.cookies.set(cookie["name"], cookie["value"])

# requets
myurl = "http://helpdesk.corp.dipostar.com/redmine/users/1076"
response = session.get(myurl)

if 'Logged in as' in str(response.text):
    print("Logged in")
else:
    print("NG")

