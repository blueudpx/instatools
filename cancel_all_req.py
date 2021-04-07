#!/usr/bin/env python3

# Cancel all pending follow requests on Instagram

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.common.exceptions import NoSuchElementException 
from instagram_private_api import Client, ClientCompatPatch 
import time 
import os
 
# === CONFIG ===
uname = "oliverhendriks_" # username
pwd = "--CENSORED--" # password
wsz = '1920x1080' # size for the chrome created window
CHROMEDRIVER_PATH = '/snap/chromium/1523/usr/lib/chromium-browser/chromedriver' # path to chrome driver
TIME_DELAY = 2 # delay to avoid UI problems
SECURE_DELAY = 20 # delay to wait
entries_ = 10 # delay implemented each entries_ times
exclusions = 'blueudp' # leave blank for no exclusions or add users separated with ";"
# =============

out_var = ''

exclusions_x = exclusions.split(';')

print('[i] Using account: ' + uname)

x = input('[%] Are you sure to continue? [y/N]: ')

continuex = 0
if(x.lower() == 'y'):
	continuex = 1
else:
	continuex = 0

if(not continuex):
	print('[i] Operation aborted!')
	exit()

options = Options() 
options.add_argument('--window-size=' + wsz) 
options.add_argument('--incognito') 
chromedriver_path = CHROMEDRIVER_PATH

browser = webdriver.Chrome(executable_path=chromedriver_path, options=options) #Star Browser 
browser.get("https://www.instagram.com/") 

time.sleep(TIME_DELAY) 

print('[*] Accepting cookies message...')

accept_cookies = browser.find_element_by_xpath ('//button[text()="Accept"]') 
accept_cookies.click() 

username=browser.find_element_by_name ("username") 
username.send_keys (uname) 
password =browser.find_element_by_name ("password") 
password.send_keys(pwd) 

login_button = browser.find_element_by_xpath ("//button[@type='submit']") 
login_button.click() 

print('[*] Logging in...')

time.sleep(TIME_DELAY)

print('[*] Retrieving current follow resquests list...')

browser.get("https://www.instagram.com/accounts/access_tool/current_follow_requests") 

while True: 
	try: 
		vm_button = browser.find_element_by_xpath ("//button[@type='button']") 
		vm_button.click() 
		time.sleep(2) 
	except NoSuchElementException: 
		break
		
cfreq_source = browser.find_elements_by_xpath("//div[@class='-utLf']")  

for x in cfreq_source: 
	out_var += x.text + '\n'

browser.quit() 

api = Client(uname, pwd) 
np = out_var.split('\n')
i = 0
for x in np:
	if(i % entries_ == 0 and i != 0):
		print('[i] Waiting ' + str(SECURE_DELAY) + ' seconds before continuing for security reasons...')
		time.sleep(SECURE_DELAY)
	if(x in exclusions_x):
		print('[i] User ' + x + ' is present in exclusion list. skipping...')
		continue
	try:
		if bool(x): 
			user_info = api.username_info(x) 
			uid = user_info['user']['pk'] 
			api.friendships_destroy(uid) 
			print('[+] Cancelled follow: ' + x)
	except:
		print('[-] Something went wrong with: ' + x)
		continue
	i += 1

print('[+] Cancelled ' + str(i) + ' follow requests!')

