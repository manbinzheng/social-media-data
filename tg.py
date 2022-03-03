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

login_url = 'https://web.telegram.org/'

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
	while 1:
		if getElementByClass('SearchInput'):
			print('登录成功了！')
			break;
		if getElementByClass('input-search'):
			print('登录成功了！')
			break;
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
		json_info = json.loads(row[2])
		count = 0
		if json_info and 'telegram' in json_info.keys():
			# if count==0:
			# 	count = count+1;
			# 	continue
			browser.get(json_info['telegram'])
			time.sleep(3)
			click(getElementByXpath('//span[contains(text(), "Open in Web")]/..'))
			time.sleep(3)
			group_name = ''
			if getElementByXpath('//span[contains(text(), "SUBSCRIBE")]/../../../div/div/div/div/div/span'):
				group_name = getElementByXpath('//span[contains(text(), "SUBSCRIBE")]/../../../div/div/div/div/div/span').text
				print("群名："+group_name)
				bindToRedis(group_name,row[1])
				if getElementByXpath('//span[contains(text(), "SUBSCRIBE")]/..'):
					click(getElementByXpath('//span[contains(text(), "SUBSCRIBE")]/..'))
					print("点击 SUBSCRIBE 按钮")
			if not group_name and getElementByXpath('//button[contains(text(), "Join Group")]/../../../div/div/div/div/div/div/h3'):
				group_name = getElementByXpath('//button[contains(text(), "Join Group")]/../../../div/div/div/div/div/div/h3').text
				print("群名："+group_name)
				bindToRedis(group_name,row[1])
				if getElementByXpath('//button[contains(text(), "Join Group")]'):
					click(getElementByXpath('//button[contains(text(), "Join Group")]'))
					print("点击 Join Group 按钮")
			time.sleep(10)
browser = webdriver.Chrome()
browser.get(login_url)
input('随机键继续')
browser.get('https://t.me/splinterlands')
input('随机键继续')
start_thread(getTgLink)


