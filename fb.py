from selenium import webdriver
import time
from datetime import timedelta, datetime
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import traceback
import pyperclip
from tkinter import *
import tkinter
import tkinter.messagebox
import threading
import os
import sys
import importlib
import pymysql
import json
from selenium.webdriver.support import expected_conditions as EC
import redis

# from ./address/+time.strftime('%m%d',time.localtime(time.time()))+'.py' import address

login_url = 'https://www.facebook.com/login'

def click(elem):
	if not elem:
		return
	try:
		browser.execute_script("arguments[0].click();", elem)
	except BaseException:
		elem.click()
def getElementByXpath(xpath,t=5):
	count = 0
	while 1:
		count = count+1
		try:
			element = browser.find_element_by_xpath(xpath)
		except BaseException:
			print("找不到元素:"+xpath+"，正在重试...")
			if count>t:
				print("多次找不到元素，可能是页面错误，放弃寻找")
				return None
			time.sleep(1)
		else:
			return element

def getElementByClass(xpath,t=5):
	count = 0
	while 1:
		count = count+1
		try:
			element = browser.find_element_by_class_name(xpath)
		except BaseException:
			print("找不到元素:"+xpath+"，正在重试...")
			if count>t:
				print("多次找不到元素，可能是页面错误，放弃寻找")
				return None
			time.sleep(1)
		else:
			return element
def start_thread(fun):
	threading.Thread(target=fun).start()
def bindToRedis(group_name,obj):
	r_db = redis.Redis(host='',
	                   port='',
	                   password='',
	                   decode_responses=True,   # decode_responses=True，写入value中为str类型，否则为字节型
	                   db='0')
	r_db.hset('telegram_map',group_name,obj)
def getTgLink():
	print('链接数据库')
	db = pymysql.connect(host='',
						 user='',
						 password='',
						 database='')
	cursor = db.cursor()
	cursor.execute("select game_name_cn,game_id,social_links from `bc_game`")
	results = cursor.fetchall()
	print(results)
	for row in results:
		try:
			t = str(int(time.time()))
			json_info = json.loads(row[2])
			count = 0
			if json_info and 'facebook' in json_info.keys():
				# if count==0:
				# 	count = count+1;
				# 	continue
				browser.get(json_info['facebook'])
				time.sleep(10)
				if getElementByXpath('//span[contains(text(), "位用户关注了")]/..'):
					fl_text = getElementByXpath('//span[contains(text(), "位用户关注了")]/..').text
					fl_text = fl_text.replace(',' , '')
					fl_text = re.findall(r'(\d+)', fl_text)[0]
					sql = "INSERT INTO bc_game_status (platform,value, game_id, update_date) VALUES ('4', '"+str(fl_text)+"', '"+str(row[1])+"', '"+t+"')"
					cursor.execute(sql)
					# 提交到数据库执行
					db.commit()
					print("fb:"+fl_text)
			if json_info and 'twitter' in json_info.keys():
				# if count==0:
				# 	count = count+1;
				# 	continue
				browser.get(json_info['twitter'])
				time.sleep(10)
				if getElementByXpath('//span[contains(text(), "关注者")]/../../span'):
					fl_text = getElementByXpath('//span[contains(text(), "关注者")]/../../span').text
					fl_text = fl_text.replace(',' , '')
					if '.' in fl_text:
						fl_text = fl_text.replace('.' , '')
						fl_text = fl_text.replace('万' , '000')
					else:
						fl_text = fl_text.replace('万' , '0000')
					fl_text = re.findall(r'(\d+)', fl_text)[0]
					sql = "INSERT INTO bc_game_status (platform,value, game_id, update_date) VALUES ('5', '"+str(fl_text)+"', '"+str(row[1])+"', '"+t+"')"
					cursor.execute(sql)
					# 提交到数据库执行
					db.commit()
					print("twitter:"+fl_text)
		except BaseException as e:
			print('出现错误，跳过' + str(e))
			continue
			
# option = webdriver.ChromeOptions()
# option.add_argument('--user-data-dir=/Users/zhengmanbin/Library/Application Support/Google/Chrome/') 
browser = webdriver.Chrome()
browser.get(login_url)
input('随机键继续')
# browser.get('https://t.me/splinterlands')
browser.get("https://twitter.com/")
input('随机键继续')
start_thread(getTgLink)


