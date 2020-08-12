from selenium.common.exceptions import NoSuchElementException #exception
import random
import hashlib

class Comments:
    def __init__(self):
        self.id=''
        self.parent=None
        self.comments=[]
    def analyze_data(self,browser):
        pass
    def get_uid(self,browser):
        pass
class Comment:
    AUTHOR='author-text'
    CONTENT='content-text'
    SREPLIES='following-sibling::*[1]'
    REPLIES='ytd-comment-renderer'
    def __init__(self,obj,r):
        self.r=r
        self.id=''
        self.obj=obj
        self.author=''
        self.content=''
        self.comments_of_comment=[]
        self.get_uid()
        self.process_author(r)
        self.process_content(r)
        self.process_replies(r)
        self.parent_id=obj.id
    def get_uid(self):
        selfid=str(id(self))+"/"
        rint=str(random.randint(0,100))+'/'
        idcode=selfid+rint
        self.id=hashlib.md5(idcode.encode()).hexdigest()
    def process_author(self,r):
        try:
            self.author=r.find_element_by_id(Comment.AUTHOR).text
        except NoSuchElementException:
            pass
    def process_content(self,r):
        try:
            self.content=r.find_element_by_id(Comment.CONTENT).text
        except NoSuchElementException:
            pass
    def process_replies(self,r):
        try:
            replies=r.find_element_by_xpath(Comment.SREPLIES)
            rs=replies.find_elements_by_tag_name(Comment.REPLIES)
            if len(rs) > 0: #if any
                for rss in rs:
                    self.comments_of_comment.append(Comment(self,rss))
        except NoSuchElementException:
            pass
class YouTubeComments(Comments):
    COMMENT='comment'
    def __init__(self):
        super().__init__()
    def get_uid(self,browser):
        url=browser.current_url+"/"
        selfid=str(id(self))+"/"
        rint=str(random.randint(0,100))+'/'
        idcode=url+selfid+rint
        self.id=hashlib.md5(idcode.encode()).hexdigest()
    def analyze_data(self,browser):
        self.get_uid(browser) #generate id
        replies=browser.find_elements_by_id(YouTubeComments.COMMENT)
        if len(replies) <=0: #nothing found
            return False
        #processing...
        for r in replies:
            comment=Comment(self,r)
            if comment.author is not '':
                self.comments.append(comment)      