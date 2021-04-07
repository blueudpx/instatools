#!/usr/bin/env python3

# Mass user following via suggestions

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.common.exceptions import NoSuchElementException 
from instagram_private_api import Client, ClientCompatPatch 
import time 
import os
 
# === CONFIG ===
uname = "oliverhendriks_" # username
pwd = "--CENSORED--" # password
SECURE_DELAY = 20 # delay to wait
entries_ = 10 # delay implemented each entries_ times
exclusions = '' # leave blank for no exclusions or add users separated with ";"
# =============

api = Client(uname, pwd) 

print('[i] Logged in as: ' + uname)

x = input('[%] Are you sure to continue? [y/N]: ')

continuex = 0
if(x.lower() == 'y'):
	continuex = 1
else:
	continuex = 0

if(not continuex):
	print('[i] Operation aborted!')
	exit()

maxx = int(input('[%] Maximum users to follow: '))

initial_user = input('[%] What user do you want the suggested people to come from?: ')

exclusions_x = exclusions.split(';')

user_info = api.username_info(initial_user) 
uid = user_info['user']['pk']

suggested = api.discover_chaining(uid)['users']
i = 0
while(True):
	for u_info in suggested:
		if(i == maxx):
			print('[i] Max users reached!')
			print('[+] Followed ' + str(i) + ' users!')
			exit()
		if(i % entries_ == 0 and i != 0):
			print('[i] Waiting ' + str(SECURE_DELAY) + ' seconds before continuing for security reasons...')
			time.sleep(SECURE_DELAY)
		if(u_info['username'] in exclusions_x):
			print('[i] User ' + u_info['username'] + ' is present in exclusion list. skipping...')
			continue
		api.friendships_create(u_info['pk'])
		print('[+] Followed: uid = ' + str(u_info['pk']) + ' ; username = ' + u_info['username'] + ' ; name = ' + u_info['full_name'])
		i += 1
print('[+] Followed ' + str(i) + ' users!')
