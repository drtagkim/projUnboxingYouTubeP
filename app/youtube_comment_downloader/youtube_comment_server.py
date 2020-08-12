import os
import io
import googleapiclient.discovery
import pandas as pd
from flask import Flask,make_response,send_file

class YouTubeCommentInt:
    def __init__(self,api_key):
        self.api_service_name='youtube'
        self.api_version='v3'
        self.api_key=api_key
        self.youtube=None
    def service_build(self):
        self.youtube=googleapiclient.discovery.build(
            self.api_service_name, 
            self.api_version, 
            developerKey = self.api_key)
    def request_build(self,next_page_token):
        pass
class YouTubeCommentFactory(YouTubeCommentInt):
    def __init__(self,api_key):
        super().__init__(api_key)
    def service_build(self):
        if self.youtube is not None:
            return
        super().service_build()
    def request_build(self,vid,next_page_token=None):
        assert self.youtube is not None,"service_build() required."
        youtube=self.youtube
        if next_page_token is not None:
            request = youtube.commentThreads().list(
                part="id,replies,snippet",
                maxResults=100,
                videoId=vid,
                pageToken=next_page_token
            )
        else:
            request = youtube.commentThreads().list(
                part="id,replies,snippet",
                maxResults=100,
                videoId=vid
            )
        return request.execute()
class Comment:
    def __init__(self,item):
        self.item=item
        #members
        self.videoId=''
        self.textDisplay=''
        self.textOriginal=''
        self.authorDisplayName=''
        self.likeCount=''
        self.publishedAt=''
        self.id=item['id']
        snippet=item['snippet']
        self.replies=[]
        #analysis
        if 'topLevelComment' in snippet:
            topLevelComment=snippet['topLevelComment']
            content=topLevelComment['snippet']
            self.parentId='TOP'
            self.totalReplyCount=snippet['totalReplyCount']
            if 'replies' in item:
                comments=item['replies']['comments']
                self.replies=[Comment(com) for com in comments]
        else:
            content=snippet
            self.parentId=content['parentId']
        if 'videoId' in content: self.videoId=content['videoId']
        if 'textDisplay' in content: self.textDisplay=content['textDisplay']
        if 'textOriginal' in content: self.textOriginal=content['textOriginal']
        if 'authorDisplayName' in content: self.authorDisplayName=content['authorDisplayName']
        if 'likeCount' in content: self.likeCount=content['likeCount']
        if 'publishedAt' in content: self.publishedAt=content['publishedAt']
def collect_comment(youtube_factory_obj,vid,verbose=True):
    result=[]
    cnt=1
    yt=youtube_factory_obj
    yt.service_build()
    v=yt.request_build(vid)
    result.append(v)
    while 'nextPageToken' in v:
        npt=v['nextPageToken']
        if verbose:
            print("{} - {}".format(cnt,npt))
        v=yt.request_build(vid,npt)
        result.append(v)
        cnt+=1
    return result
def process_raw_comment_result(rs):
    comments=[]
    for cs in rs:
        for i in cs['items']:
            comments.append(Comment(i))
    return comments
def analyze_to_pandas(comments):
    analyzed_results1={}
    analyzed_results1['id']=[i.id for i in comments]
    analyzed_results1['videoId']=[i.videoId for i in comments]
    analyzed_results1['authorDisplayName']=[i.authorDisplayName for i in comments]
    analyzed_results1['textOriginal']=[i.textOriginal for i in comments]
    analyzed_results1['likeCount']=[i.likeCount for i in comments]
    analyzed_results1['publishedAt']=[i.publishedAt for i in comments]
    analyzed_results1['parentId']=[i.parentId for i in comments]
    analyzed_results1['num_replies']=[len(i.replies) for i in comments]
    rps=[]
    for i in comments:
        if len(i.replies) > 0:
            rps+=i.replies
    analyzed_results2={}
    analyzed_results2['id']=[i.id for i in rps]
    analyzed_results2['videoId']=[i.videoId for i in rps]
    analyzed_results2['authorDisplayName']=[i.authorDisplayName for i in rps]
    analyzed_results2['textOriginal']=[i.textOriginal for i in rps]
    analyzed_results2['likeCount']=[i.likeCount for i in rps]
    analyzed_results2['publishedAt']=[i.publishedAt for i in rps]
    analyzed_results2['parentId']=[i.parentId for i in rps]
    analyzed_results2['num_replies']=[len(i.replies) for i in rps]
    analyzed=pd.concat([
        pd.DataFrame(analyzed_results1),
        pd.DataFrame(analyzed_results2)
    ])
    return analyzed
def cal_all_comments(cs):
    num1=len(cs)
    num2=sum([len(i.replies) for i in cs])
    return num1+num2
#
app=Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World"
@app.route('/<apikey>/<vid>')
def youtube_comment(apikey,vid):
    print(apikey)
    print(vid)
    yt=YouTubeCommentFactory(apikey)
    yt.service_build()
    results=collect_comment(yt,vid,verbose=True)
    comments=process_raw_comment_result(results)
    n=cal_all_comments(comments)
    analyzed=analyze_to_pandas(comments)
    analyzed.to_excel('peng_TV_sample.xlsx',index=False)
    output=io.BytesIO()
    writer=pd.ExcelWriter(output,engine='xlsxwriter')
    analyzed.to_excel(writer,'Tab1',index=False)
    writer.save()
    output.seek(0)
    print("File exported: output.xlsx")
    return send_file(output,
        attachment_filename='youtube_comment_{}.xlsx'.format(vid),
        as_attachment=True)
if __name__=='__main__':
    app.run(host='0.0.0.0',port=9999,debug=True)