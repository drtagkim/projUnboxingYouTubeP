#
#
#

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
		
