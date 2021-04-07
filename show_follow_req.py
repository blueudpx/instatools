#!/usr/bin/env python3

# Show all pending follow requests on Instagram

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.common.exceptions import NoSuchElementException 
from instagram_private_api import Client, ClientCompatPatch 
import time 
import os
 
# === CONFIG ===
uname = "oliverhendriks_" 
pwd = "--CENSORED--"
wsz = '1920x1080'
CHROMEDRIVER_PATH = '/snap/chromium/1523/usr/lib/chromium-browser/chromedriver'
TIME_DELAY = 2
# =============

out_var = ''

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
for x in np: 
	print('[*] Found follow request: ' + x)
print('[+] All done!')

