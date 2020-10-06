# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 18:17:11 2020

@author: PC
"""

import argparse #CLI
from youtubedataapi import *
import pandas as pd
from datetime import datetime
import os
parser=argparse.ArgumentParser(description="Taekyung CLI Test")
parser.add_argument('--input',required=True,help="Input file contains Video Ids")
parser.add_argument('--output',required=False,default='output.csv',help='Output file')
parser.add_argument('--key',required=True,help="YouTube Data API key")
args=parser.parse_args()
if __name__=="__main__":
    ytkey=YouTubeKey(args.key)
    ytvideo=YouTube_Video(ytkey)
    with open(args.input,'rt') as f:
        vids=[v.strip() for v in f.readlines()]
    cnt=1
    for vid in vids:
        print("[{:3d}] {}".format(cnt,vid))
        cnt+=1
        ytvideo.query({"VideoId":vid})
    w=args.output
    d=ytvideo.export_data()
    d=d[['videoId','publishedAt','viewCount','likeCount','dislikeCount','favoriteCount','commentCount']]
    d=d.assign(today=datetime.today().strftime('%Y-%m-%d_%H'))
    if os.path.exists(w):
        d.to_csv(w,index=False,mode='a',header=False)
    else:
        d.to_csv(w,index=False)
    print("Bye.")
    
    
    