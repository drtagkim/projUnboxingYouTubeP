# -*- coding: utf-8 -*-
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import pickle
class YouTubeKey:
    DEVELOPER_KEY = ""
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    def __init__(self,api_key):
        self.API_KEY=api_key
class SearchOrder:
    DATE="date",
    RATING="rating",
    RELEVANCE="relevance",
    TITLE="title",
    VIDEOCOUNT="videoCount",
    VIEWCOUNT="viewCount"
class RegionCode:
    Korea="KR",
    US="US",
    Japan="JP",
    Australia="AU",
    Austria="AT",
    Belgium="BE",
    Canada="CA",
    Chile="CL",
    Colombia="CO",
    CzechR="CZ",
    Denmark="DK",
    Estonia="EE",
    Finland="FI",
    France="FR",
    Germany="DE",
    Greece="GR",
    Hungary="HU",
    Iceland="IS",
    Ireland="IE",
    Israel="IL",
    Italy="IT",
    Latvia="LV",
    Lithuania="LT",
    Luxembourg="LU",
    Mexico="MX",
    Netherlands="NL",
    NewZealand="NZ",
    Norway="NO",
    Poland="PL",
    Portugal="PT",
    SlovakR="SK",
    Slovenia="SI",
    Spain="ES",
    Sweden="SE",
    Switzerland="CH",
    Turkey="TR",
    UnitedKingdom="GB"
class Type:
    CHANNEL="channel",
    PLAYLIST="playlist",
    VIDEO="video"
class Caption:
    ANY="any",
    CAP="closedCaption",
    NON="none"
def getRFC3339(s):
    return s+"T00:00:00Z"
class YouTube:
    def __init__(self,yt):
        self.setup(yt)
        self.options={}
        self.data=[]
        self.current_result=None
    def setup(self,yt):
        self.youtube=build(YouTubeKey.YOUTUBE_API_SERVICE_NAME,
                     YouTubeKey.YOUTUBE_API_VERSION,
                     developerKey=yt.API_KEY)
    def load_work(self,file_name):
        with open(file_name,'rb') as f:
            (options,data)=pickle.load(f)
        self.data=data
        self.options=options
    def save_work(self,file_name):
        with open(file_name,'wb') as f:
            pickle.dump((self.options,self.data),f)
    def update_options(self,new_opt):
        for k in new_opt.keys():
            self.options[k]=new_opt[k]
    def clear_options(self):
        self.options={}
    def empty_data(self):
        self.data=[]
    def export_data(self):
        return pd.concat(self.data,ignore_index=True)
    def collect_data(self,result):
        pass
    def query(self,options=None):
        pass
    def next_page(self):
        pass
class YouTube_Video(YouTube):
    def __init__(self,yt):
        super().__init__(yt)
    def query(self,options=None):
        youtube=self.youtube
        if options is not None:
            self.update_options(options)
        options=self.options
        response=youtube.videos().list(
            part='id,snippet, contentDetails, statistics, status',
            id=options['VideoId'],
            maxResults=50
            ).execute()
        self.collect_data(response)
        self.current_result=response
    def append_empty(self,fname):
        self.export_data().to_csv(fname,mode='a',header=False,index=False)
    def collect_data(self,result):
        output={}
        item=result['items'][0]
        output['videoId']=item['id']
        output['publishedAt']=item['snippet']['publishedAt']
        output['channelId']=item['snippet']['channelId']
        output['title']=item['snippet']['title']
        output['description']=item['snippet']['description']
        output['channelTitle']=item['snippet']['channelTitle']
        output['tags']=",".join(item['snippet']['tags'])
        output['categoryId']=item['snippet']['categoryId']
        output['liveBroadcastContent']=item['snippet']['liveBroadcastContent']
        output['duration']=item['contentDetails']['duration']
        output['dimension']=item['contentDetails']['dimension']
        output['definition']=item['contentDetails']['definition']
        output['caption']=item['contentDetails']['caption']
        output['licensedContent']=item['contentDetails']['licensedContent']
        output['contentRating']=item['contentDetails']['contentRating']
        output['projection']=item['contentDetails']['projection']
        output['uploadStatus']=item['status']['uploadStatus']
        output['privacyStatus']=item['status']['privacyStatus']
        output['license']=item['status']['license']
        output['embeddable']=item['status']['embeddable']
        output['publicStatsViewable']=item['status']['publicStatsViewable']
        output['madeForKids']=item['status']['madeForKids']
        output['viewCount']=item['statistics']['viewCount']
        output['likeCount']=item['statistics']['likeCount']
        output['dislikeCount']=item['statistics']['dislikeCount']
        output['favoriteCount']=item['statistics']['favoriteCount']
        output['commentCount']=item['statistics']['commentCount']
        o2=pd.DataFrame(output,index=('0',))
        self.data.append(o2)
class YouTube_Search(YouTube):
    def __init__(self,yt):
        super().__init__(yt)
    def collect_data(self,result):
        output=[]
        for item in result['items']:
            try:
                videoId=item['id']['videoId']
                snippet=item['snippet']
                if "thumbnails" in snippet:
                    snippet.pop('thumbnails')
                if "liveBroadcastContent" in snippet:
                    snippet.pop('liveBroadcastContent')
                snippet['videoId']=videoId
                if 'regionCode' in self.options:
                    snippet['regionCode']=self.options['regionCode']
                else:
                    snippet['regionCode']='NA'
                output.append(snippet)
            except:
                pass
        o2=pd.DataFrame(output)
        o2['query']=self.options['q']
        self.data.append(o2)
    def query(self,options=None):
        youtube=self.youtube
        if options is not None:
            self.update_options(options)
        options=self.options
        if 'pageToken' not in options:
            if 'publishedAfter' not in options:
                if 'publishedBefore' not in options:
                    if 'regionCode' not in options:
                        search_response=youtube.search().list(
                            q=options['q'],
                            part='id,snippet',
                            maxResults=options['max_results']
                        ).execute()
                    else:
                        search_response=youtube.search().list(
                            q=options['q'],
                            part='id,snippet',
                            maxResults=options['max_results'],
                            regionCode=options['regionCode']
                        ).execute()
                else:
                    if 'regionCode' not in options:
                        search_response=youtube.search().list(
                            q=options['q'],
                            part='id,snippet',
                            maxResults=options['max_results'],
                            publishedBefore=options['publishedBefore']
                        ).execute()
                    else:
                        search_response=youtube.search().list(
                            q=options['q'],
                            part='id,snippet',
                            maxResults=options['max_results'],
                            regionCode=options['regionCode'],
                            publishedBefore=options['publishedBefore']
                        ).execute()
            else:
                if 'publishedBefore' not in options:
                    if 'regionCode' not in options:
                        search_response=youtube.search().list(
                            q=options['q'],
                            part='id,snippet',
                            maxResults=options['max_results'],
                            publishedAfter=options['publishedAfter']
                        ).execute()
                    else:
                        search_response=youtube.search().list(
                            q=options['q'],
                            part='id,snippet',
                            maxResults=options['max_results'],
                            regionCode=options['regionCode'],
                            publishedAfter=options['publishedAfter']
                        ).execute()
                else:
                    if 'regionCode' not in options:
                        search_response=youtube.search().list(
                            q=options['q'],
                            part='id,snippet',
                            maxResults=options['max_results'],
                            publishedBefore=options['publishedBefore'],
                            publishedAfter=options['publishedAfter']
                        ).execute()
                    else:
                        search_response=youtube.search().list(
                            q=options['q'],
                            part='id,snippet',
                            maxResults=options['max_results'],
                            regionCode=options['regionCode'],
                            publishedBefore=options['publishedBefore'],
                            publishedAfter=options['publishedAfter']
                        ).execute()
        else:
            if 'publishedAfter' not in options:
                if 'publishedBefore' not in options:
                    if 'regionCode' not in options:
                        search_response=youtube.search().list(
                            q=options['q'],
                            part='id,snippet',
                            maxResults=options['max_results'],
                            pageToken=options['pageToken']
                        ).execute()
                    else:
                        search_response=youtube.search().list(
                            q=options['q'],
                            part='id,snippet',
                            maxResults=options['max_results'],
                            regionCode=options['regionCode'],
                            pageToken=options['pageToken']
                        ).execute()
                else:
                    if 'regionCode' not in options:
                        search_response=youtube.search().list(
                            q=options['q'],
                            part='id,snippet',
                            maxResults=options['max_results'],
                            publishedBefore=options['publishedBefore'],
                            pageToken=options['pageToken']
                        ).execute()
                    else:
                        search_response=youtube.search().list(
                            q=options['q'],
                            part='id,snippet',
                            maxResults=options['max_results'],
                            regionCode=options['regionCode'],
                            publishedBefore=options['publishedBefore'],
                            pageToken=options['pageToken']
                        ).execute()
            else:
                if 'publishedBefore' not in options:
                    if 'regionCode' not in options:
                        search_response=youtube.search().list(
                            q=options['q'],
                            part='id,snippet',
                            maxResults=options['max_results'],
                            publishedAfter=options['publishedAfter'],
                            pageToken=options['pageToken']
                        ).execute()
                    else:
                        search_response=youtube.search().list(
                            q=options['q'],
                            part='id,snippet',
                            maxResults=options['max_results'],
                            regionCode=options['regionCode'],
                            publishedAfter=options['publishedAfter'],
                            pageToken=options['pageToken']
                        ).execute()
                else:
                    if 'regionCode' not in options:
                        search_response=youtube.search().list(
                            q=options['q'],
                            part='id,snippet',
                            maxResults=options['max_results'],
                            publishedBefore=options['publishedBefore'],
                            publishedAfter=options['publishedAfter'],
                            pageToken=options['pageToken']
                        ).execute()
                    else:
                        search_response=youtube.search().list(
                            q=options['q'],
                            part='id,snippet',
                            maxResults=options['max_results'],
                            regionCode=options['regionCode'],
                            publishedBefore=options['publishedBefore'],
                            publishedAfter=options['publishedAfter'],
                            pageToken=options['pageToken']
                        ).execute()
        self.collect_data(search_response)
        self.current_result=search_response
    def next_page(self):
        result=self.current_result
        if result is not None:
            if 'nextPageToken' in result:
                self.update_options({'pageToken':result['nextPageToken']})
                return True
        return False
