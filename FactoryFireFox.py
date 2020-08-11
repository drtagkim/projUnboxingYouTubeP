# FactoryFireFox.py
# Author: Taekyung Kim(kimtk@office.kw.ac.kr)
# First created on 6 Aug 2020
# Last updated on 11 Aug 2020
# YouTube Data Collection
# Dependencies:
#  pip install selenium
#  pip install bs4
# Install Firefox first.

from selenium import webdriver #webdriver
from selenium.webdriver.firefox.options import Options #Firefox options
from selenium.webdriver.common.keys import Keys #key emulation
from bs4 import BeautifulSoup as BS
# utility
import time

#' Firefox factor, inherited from webdriver.Firefox
class FactoryFirefoxDriver(webdriver.Firefox):
    def __init__(self,headless=False,image_allow=True):
        options=Options()
        profile=webdriver.FirefoxProfile()
        profile.set_preference('permissions.default.image',1 if image_allow else 2)
        options.headless=headless #headless mode on?
        super().__init__(firefox_profile=profile,options=options)
#' Webdriver for YouTube comment collection
#' >>> b=YouTubeCommentBrowser(headless=True,image_allow=False)
#' >>> b.visit("some YouTube video URL")
#' >>> comments=b.collect_comments(verbose=True)
#' >>> b.quit() #session close.
#' 
class YouTubeCommentBrowser(FactoryFirefoxDriver):
    def __init__(self,headless=False,image_allow=True):
        super().__init__(headless,image_allow)
    def press_down(self,h,tb=1):
        h.send_keys(Keys.END)
        time.sleep(tb)
    def scroll_down(self,tb=1):
        initial_height = self.execute_script("return window.scrollY")
        html=self.find_element_by_tag_name('html')
        self.press_down(html,tb)
        time.sleep(tb)
        #self.press_down(html)
        last_height = self.execute_script("return window.scrollY")
        if initial_height == last_height:
            return False
        while True:
            time.sleep(tb)
            new_height=self.execute_script("return window.scrollY")
            if new_height==last_height:
                break
            last_height=new_height
        return True
    def remove_element_by_id(self,s,tb=0.5):
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
        code_view='//yt-formatted-string[starts-with(.,"View") and contains(.,"reply")]'
        code_show_more_replies='//yt-formatted-string[starts-with(.,"View") and contains(.,"replies")]'
        eles=self.find_elements_by_xpath(code_view)
        for ele in eles:
            try:
                if ele.text is not "":
                    ele.click()
                    time.sleep(0.1)
            except:
                pass
        eles=self.find_elements_by_xpath(code_show_more_replies)
        for ele in eles:
            try:
                if ele.text is not "":
                    ele.click()
                    time.sleep(0.1)
            except:
                pass
        time.sleep(tb)
    def text_more(self,tb=1):
        code_read_more='//span[starts-with(.,"Read more")]'
        eles=self.find_elements_by_xpath(code_read_more)
        for ele in eles:
            try:
                if ele.text is not "":
                    ele.click()
                    time.sleep(0.1)
            except:
                pass
        time.sleep(tb)
    def visit(self,url,remove_ad=True,remove_player=True,tb=5):
        self.get(url)
        time.sleep(tb)
        if remove_ad:
            self.remove_element_by_id('related')
            time.sleep(0.1)
        if remove_player:
            self.remove_element_by_id('movie_player')
            time.sleep(0.1)
    def get_data(self):
        page=self.page_source
        soup=BS(page,'html.parser')
        return [ele.text for ele in soup.select('#content-text')]
    def collect_comments(self,verbose=False,remove_previous=True):
        total_comment=[] # //TODO - bs4
        if verbose:
            print("Start.")
        while True:
            if verbose:
                print("..Scroll down")
            if self.scroll_down(3) is False:
                break
            if verbose:
                print("..Call more replies, read more")
            for i in range(3):
                self.reply_more()
            self.text_more()
            if verbose:
                print("..Collect data")
                
            if remove_previous:
                if verbose:
                    print("..Remove previous comments in the browser")
                total_comment+=self.get_data()
                self.remove_comments()
        if remove_previous is False:
            total_comment=self.get_data()
        if verbose:
            print("Done.")
        return total_comment
