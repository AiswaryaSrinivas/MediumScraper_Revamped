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
        
        #Towards Data Science Cookie, set your own
        
        tds_cookie={
                              
 }
        #HackerNoon Cookie
        
       #set  your owu 
        cookie={   
        
                                  }
        
                                  
        header = {
                     
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
        
        
        
   

                    
                    
        
        
        

    

