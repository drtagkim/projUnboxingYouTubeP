from youtube_transcript_api import YouTubeTranscriptApi
class YouTubeCC:
    def __init__(self,video_id):
        self.video_id=video_id
        self.lang=['en',]
        try:
            transcription_list=YouTubeTranscriptApi.list_transcripts(self.video_id)
            gencc=transcription_list.find_generated_transcript(['en',])
            self.content=gencc.fetch()
        except:
            print("Error!")
    def get_content(self):
        output=None
        try:
            output=self.content
        except:
            pass
        return output
    def get_cc(self):
        item=None
        try:
            item_list=[pd.DataFrame(r,index=[0]) for r in self.content]
            item=pd.concat(item_list)
            item=item.reset_index()
            del item['index']
            item['video_id']=self.video_id
            self.cc=item
        except:
            pass
        return item