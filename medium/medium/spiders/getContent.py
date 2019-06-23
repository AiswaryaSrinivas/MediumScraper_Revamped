# -*- coding: utf-8 -*-
"""
Created on Tue May  1 23:30:54 2018

@author: Aiswarya

This scrapper extracts data for a given date and a given tag

scrapy crawl -a start_date=20170901 -a end_date=20180930 -a tagSlug='machine-learning data-science artificial-intelligence ai' -o "data//medium_scrapper_%(item_name)s.csv" -t csv  medium_scrapper 



scrapy crawl -a start_date=20180820 -a end_date=20180820 -a tagSlug='machine-learning' -o "data//medium_scrapper_%(item_name)s.csv" -t csv  medium_scrapper 

https://medium.com/s/story/machine-learning-to-predict-taxi-fare-part-two-predictive-modelling-f80461a8072e

 '''
        if response.status==302:
          
            print("redirecting")
            
            url=response.headers['Location'].decode('utf-8')    
            r=requests.get(url)
            data=r.text
            data_split=data.split('<![CDATA[\nwindow["obvInit"](')
            data=data_split[len(data_split)-1]
            data=data.split(")\n// ]]>")[0]
            dat=demjson.decode(data)
            
            dat_final=json.dumps(str(dat))
            writeTofile(folder_path+str(post_id)+"_"+str(tag)+".json",dat_final)
        '''  
"""

import scrapy
import codecs
import json#
from datetime import datetime
from datetime import timedelta
import os
from medium.items import PostsItem,TagsItem,UserItem,CollectionItem,ContentItem
from medium.utilities import Medium
import requests
from bs4 import BeautifulSoup
from codecs import raw_unicode_escape_decode
import demjson
import pandas as pd
def writeTofile(fileName,text):
    with codecs.open(fileName,'w','utf-8') as outfile:
        outfile.write(text)


class MediumPost(scrapy.Spider):
    name='medium_scrapper_content'
    handle_httpstatus_list = [401,400,409]
    autothrottle_start_delay=10
    autothrottle_enabled=True
    def start_requests(self):
        data=pd.read_csv("/Users/aiswarya/DataScienceArena/medium/outputs/Repull_Jan_2019.csv",encoding='utf-8')
        #data=data.loc[pd.notnull(data['uniqueSlug'])]
        #data['story_url_other']=data['uniqueSlug'].apply(lambda x:"https://medium.com/s/story/"+x)
        start_urls=data['url'].tolist()
        print(start_urls)
        #start_urls=['https://chatbotslife.com/building-a-simple-chatbot-using-dialogflow-99c7ecf60566']
        ids=data['postId'].tolist()
        #ids=['99c7ecf60566']
        #start_urls = ['https://medium.com/tag/'+self.tagSlug.strip("'")+'/archive/']
        print(len(start_urls))
        
        #Towards Data Science Cookie
        
        tds_cookie={
                               '__cfduid':'d74571b7cc34a03a824fa032112ad94af1522260237',
 '_ga':'GA1.2.113405192.1522260242',
 'uid':'7bbdad3b3571',
 #'sid': '1:DwJl0+iLALCggauelHDqXaaw7GG3ipuiZ0iUd4DDteP+F/lt6J/3sxYV+VXy+XIT',
 #'sid':'1:tI92Vf9R8FBe+aBWRN2n4VLtYH8xR3jxhQBUClCSvyxSzPBloyxi3xhigLCTd6yh',
 #'sid':'1:8SPoQh4B4P7f/DbVWt6lDvHo6t2UAQlTiJUUdMUkIAectgJOw7aqFEQ5eKcB0BJV',
 #'sid':'1:DKSJT0fPDKWWprJzaIUVOAQVryMSZMnXdj/qQqVBWYIZT4/5l6U/M0QT8Rx4uKqW32dmeh1o2JmwlhZZZW8Z/g==',
 'lightstep_guid/medium-web':'e64e13b22fb98a54',
 'lightstep_session_id':'39dc1b5e47a62082',
 'pr':'2', 
 'tz':'-330',
 'lightstep_guid/lite-web':'1a533fe15c9c46c8',
 '_gid':'GA1.2.1151037376.1538835202',
 'xsrf':'GkW4aZZB3TvA72jQ',
 '_parsely_session':'{%22sid%22:84%2C%22surl%22:%22https://towardsdatascience.com/a-data-science-for-good-machine-learning-project-walk-through-in-python-part-one-1977dd701dbc%22%2C%22sref%22:%22%22%2C%22sts%22:1541615052543%2C%22slts%22:1541609666358}; _parsely_visitor={%22id%22:%22pid=3b6e4394824702274089e2bcbabd0a63%22%2C%22session_count%22:84%2C%22last_session_ts%22:1541615052543}', 
 'sz':'792'
 }
        #HackerNoon Cookie
        
        wearefuturegov_sid='1:/7IrChqirJ31pM0ODUbLgECatf1jvZMoV0mkv/efG/BnNIjTTGJIEOI8pUt7055pwygX3ihHRPsAlJ9ndn19Vg=='
        markgrowth_sid='1:YwxbJRr2Kqp3Ta86BWmvyvYDPW3lMaqwEYf7C3KumwqFFeXBKDbt1WmFkNiNKr4t'
        hackernoon_sid="1:DwJl0+iLALCggauelHDqXaaw7GG3ipuiZ0iUd4DDteP+F/lt6J/3sxYV+VXy+XIT"
        cookie={
                               '__cfduid':'d74571b7cc34a03a824fa032112ad94af1522260237',
 '_ga':'GA1.2.1247018129.1539972035',
 'uid':'7bbdad3b3571',
 'sid':'1:DwJl0+iLALCggauelHDqXaaw7GG3ipuiZ0iUd4DDteP+F/lt6J/3sxYV+VXy+XIT',
 'lightstep_guid/medium-web':'6e80f904c2ad8a05',
 'lightstep_session_id':'2cc53cae85a476ca',
 'pr':'2', 
 'tz':'-330',
 'lightstep_guid/lite-web':'1a533fe15c9c46c8',
 '_gid':'GA1.2.1151037376.1538835202',
 'xsrf':'J4gwC2lOfTOIdUCA',
 '_parsely_session':'{%22sid%22:8%2C%22surl%22:%22https://hackernoon.com/numpy-with-python-for-data-science-16ff2f646591%22%2C%22sref%22:%22%22%2C%22sts%22:1541618234349%2C%22slts%22:1541270584773}; _parsely_visitor={%22id%22:%22pid=3b6e4394824702274089e2bcbabd0a63%22%2C%22session_count%22:8%2C%22last_session_ts%22:1541618234349}', 
 'sz':'556'        
        
                                  }
        
                                  
        header = {
                        'accept': 'application/json',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'en-US,en;q=0.9,ta;q=0.8',
                        'content-type': 'application/json',
                        'referer': 'https://medium.com/',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
                        'x-client-date': '1525197603242',
                        'x-obvious-cid': 'web',
                        'x-opentracing': '{"ot-tracer-spanid":"4f6cec2cae2d3","ot-tracer-traceid":"10856221151cfe","ot-tracer-sampled":"true"}',
                        'x-xsrf-token': 'wpVeJB2qz9QG',
                        'path': '/numpy-with-python-for-data-science-16ff2f646591',
                        'authority':'hackernoon.com'
        }   
        #start_date=self.start_date
        #end_date=self.end_date
        #startDate=datetime.strptime(self.start_date,"%Y%m%d")
        #endDate=datetime.strptime(self.end_date,"%Y%m%d")
        #delta=endDate-startDate
        #print delta
        #foldername="inputs"
        #for i in range(delta.days + 1):
            #d=datetime.strftime(startDate+timedelta(days=i),'%Y/%m/%d')
        count=0
        for url in start_urls:
            print(url)
            if "towardsdatascience" in url:
                yield scrapy.Request(url,method="GET",headers=header,cookies=tds_cookie,callback=self.parse_story,meta={'id':ids[count],'url':url})
            if "hackernoon" in url:
                cookie['sid']=hackernoon_sid
                yield scrapy.Request(url,method="GET",headers=header,cookies=cookie,callback=self.parse_story,meta={'id':ids[count],'url':url})
            if "wearefuturegov" in url:
                cookie['sid']=wearefuturegov_sid
                yield scrapy.Request(url,method="GET",headers=header,cookies=cookie,callback=self.parse_story,meta={'id':ids[count],'url':url})
            if "markgrowth" in url:
                cookie['sid']=markgrowth_sid
                yield scrapy.Request(url,method="GET",headers=header,cookies=cookie,callback=self.parse_story,meta={'id':ids[count],'url':url})
            
            
            count=count+1
    

    
        
    def parse_story(self,response):
        folder=datetime.now().strftime("%Y%m%d")
        folder_path=folder+"//text//" 
        post_id=response.meta['id']
        response_data=response.text
        try:
            
            response_split=response_data.split("while(1);</x>")
            response_data=response_split[1]
            


            scrappedDate=folder
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)        
        
        
            writeTofile(folder_path+str(post_id)+"_.json",response_data)  
        
            medium=Medium(folder_path+str(post_id)+"_.json")
        
            data=medium.getJsonResponse()
            contentitem=ContentItem()
            contentitem=medium.processContent(data,contentitem)
            contentitem['postId']=post_id
            contentitem['scrappedDate']=scrappedDate
            contentitem['url']=response.meta['url']
            yield contentitem
        except:
            writeTofile(folder_path+str(post_id)+"_.txt",response_data)  
        
        
        
   

                    
                    
        
        
        

    

