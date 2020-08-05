# FactoryFireFox.py
# Author: Taekyung Kim(kimtk@office.kw.ac.kr)
# First created on 6 Aug 2020
# YouTube Data Collection

from selenium import webdriver #웹드라이브
from selenium.webdriver.firefox.options import Options #Firefox options
from selenium.webdriver.common.keys import Keys #key emulation
from bs4 import BeautifulSoup as BS
# utility
import time

class FactoryFireFoxDriver(webdriver.Firefox):
	def __init__(self,headless=False,image_allow=True):
		options=Options()
		profile=webdriver.FirefoxProfile()
		profile.set_preference('permissions.default.image',1 if image_allow else 2)
		options.headless=headless
		super().__init__(firefox_profile=profile,options=options)

class YouTubeCommentBrowser(FactoryFireFoxDriver):
	def __init__(self,headless=False,image_allow=True):
		super().__init__(headless,image_allow)
	def press_down(self,tb=1):
		self.send_keys(Keys.END)
		time.sleep(tb)
	def remove_element_by_id(self,tb=0.5):
		script="document.getElementById('{}').remove();".format(s)
		self.execute_script(script)
		time.sleep(tb)
	def remove_comments(self,tb=0.5):
		script='''
		document.querySelectorAll("#replies").forEach(function(item,index){item.remove();});
		var reviews=document.querySelectorAll('#body');
		reviews.forEach(function(item,index){
		if(index<(reviews.length-1)) item.remove();
		})
		'''
		self.execute_script(script)
		time.sleep(tb)
	def reply_more(self,tb=1):
		code_view='//yt-formatted-string[contains(.,"View")]'
		code_show_more_replies='//yt-formatted-string[contains(."Show more replies")]'
		eles=self.find_elements_by_xpath(code_view)
		for ele in eles:
			if ele.text is not "":
				ele.click()
				time.sleep(0.1)
		eles=self.find_elements_by_xpath(code_show_more_replies)
		for ele in eles:
			if ele.text is not "":
				ele.click()
				time.sleep(0.1)
		time.sleep(tb)
	def text_more(self,tb=1):
		code_read_more='//span[contains(.,"Read more")]'
		self.find_elements_by_xpath(code_read_more)
		for ele in eles:
			if ele.text is not "":
				ele.click()
				time.sleep(0.1)
		time.sleep(tb)
