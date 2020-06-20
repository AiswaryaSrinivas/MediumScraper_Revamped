# -*- coding: utf-8 -*-
"""
Created on Tue May  1 23:30:54 2018

@author: Aiswarya

This scrapper extracts data for a given date and a given tag

scrapy crawl -a start_date=20170901 -a end_date=20180930 -a tagSlug='machine-learning data-science artificial-intelligence ai' -o "data//medium_scrapper_%(item_name)s.csv" -t csv  medium_scrapper 

scrapy crawl -o"data//medium_scrapper_content_HackerNoon%(item_name)s.csv" -t csv medium_scrapper_content


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
    name='medium_scrapper'
    handle_httpstatus_list = [401,400]
    autothrottle_start_delay=10
    autothrottle_enabled=True
    def start_requests(self):
        tagSlug=self.tagSlug.strip("'")
        tags=tagSlug.split()
        start_urls=[]
        for tag in tags:
            start_urls.append('https://medium.com/tag/'+tag+'/archive/')
        #print(start_urls)
        
        cookie={
                                  } ## set your own cookie
        header = {
                        'accept': 'application/json',
                        'accept-encoding': 'gzip, deflate, br',
                        'accept-language': 'en-US,en;q=0.9,ta;q=0.8',
                        'content-type': 'application/json',
                        'referer': 'https://medium.com/tag/data-science/archive/2018/03/23',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
                        'x-client-date': '1525197603242',
                        'x-obvious-cid': 'web',
                        'x-opentracing': '{"ot-tracer-spanid":"1cbe927d0f29e9","ot-tracer-traceid":"8f0a5b5308eab","ot-tracer-sampled":"true"}',
                        'x-xsrf-token': 'hBL2qH8I5ckb'
        }   
        #start_date=self.start_date
        #end_date=self.end_date
        startDate=datetime.strptime(self.start_date,"%Y%m%d")
        endDate=datetime.strptime(self.end_date,"%Y%m%d")
        delta=endDate-startDate
        #print delta
        #foldername=self.folder
        for i in range(delta.days + 1):
            d=datetime.strftime(startDate+timedelta(days=i),'%Y/%m/%d')
            for url in start_urls:
                #print url+d
                tag=url.replace("/archive/","")
                tag=tag.replace("https://medium.com/tag/","")
                
                yield scrapy.Request(url+d,method="GET",headers=header,cookies=cookie,callback=self.parse,meta={'reqDate':d,'tag':tag})
        
        #for url in start_urls:
            #yield scrapy.Request(url,method='GET',headers=header,cookies=cookie,callback=self.parse)
            #yield scrapy.Request(url,method='GET',body=json.dumps(formdata),headers=header,cookies=cookie,callback=self.parse)
    
    

    
        
    def parse_story(self,response):
        
        response_data=response.text
        response_split=response_data.split("while(1);</x>")
        response_data=response_split[1]
        #header=response.meta['id']
        #cookie=response.meta['cookie']
        post_id=response.meta['id']
        folder_path=response.meta['folderpath']+"//text//"
        tag=response.meta['tag']
        scrappedDate=response.meta['folderpath']
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)        
        
        
        writeTofile(folder_path+str(post_id)+"_"+str(tag)+".json",response_data)   
        medium=Medium(folder_path+str(post_id)+"_"+str(tag)+".json")
        
        data=medium.getJsonResponse()
        contentitem=ContentItem()
        contentitem=medium.processContent(data,contentitem)
        contentitem['postId']=post_id
        contentitem['scrappedDate']=scrappedDate
        contentitem['url']=response.meta['url']
        yield contentitem
        
        
        
    
    def parse(self,response):
        response_data=response.text
        if response.status==302:
            writeTofile("GatewayException.txt",response.text)
            #print(response.text)
            
        response_split=response_data.split("while(1);</x>")
        if len(response_split)>1:
            response_data=response_split[1]
        
        date_post=response.meta['reqDate']
        date_post=date_post.replace("/","")
        #directory=response.meta['folder']
        directory=datetime.now().strftime("%Y%m%d")
        scrappedDate=directory
        if response.status==504:
            writeTofile("GatewayException.txt",tag.replace("-","").strip("'")+"Tag"+date_post+"\n")
        if not os.path.exists(directory):
            os.makedirs(directory)
        tag=response.meta['tag']
        file_path=directory+"//"+tag.replace("-","").strip("'")+"Tag"+date_post+".json"
        
        writeTofile(directory+"//"+tag.replace("-","").strip("'")+"Tag"+date_post+".json",response_data)
        #Check if the status in json file is success. 
        
        cookie={
                               '__cfduid':'d74571b7cc34a03a824fa032112ad94af1522260237',
 '_ga':'GA1.2.113405192.1522260242',
 'uid':uid,
 'sid':sid,
 'lightstep_guid/medium-web':'ebfeabd79fbebc5',
 'lightstep_session_id':'65ab062ac2ff3cd3',
 'pr':'1', 
 'tz':'-330',
 'lightstep_guid/lite-web':'1a533fe15c9c46c8',
 '_gid':'GA1.2.1144733218.1535656850',
 'xsrf':'wpVeJB2qz9QG',
 '_parsely_session':'{%22sid%22:139%2C%22surl%22:%22https://medium.com/analytics-vidhya/machine-learning-to-predict-taxi-fare-part-one-exploratory-analysis-6b7e6b1fbc78?source=user_profile---------2------------------%22%2C%22sref%22:%22https://medium.com/@aiswaryar%22%2C%22sts%22:1535806673741%2C%22slts%22:1535796673424}; _parsely_visitor={%22id%22:%22e06be823-512c-4d27-af50-9948cae8a366%22%2C%22session_count%22:139%2C%22last_session_ts%22:1535806673741}', 
 'sz':'424', 
 '_gat':'1', 
 '_parsely_slot_click':'{%22url%22:%22https://medium.com/%22%2C%22x%22:16%2C%22y%22:273%2C%22xpath%22:%22//*[@id=%5C%22_obv.shell._surface_1535807533173%5C%22]/div[1]/div[3]/div[1]/div[1]/section[1]/div[1]/div[1]/div[1]/div[1]/a[1]%22%2C%22href%22:%22https://medium.com/s/story/to-make-your-business-more-efficient-take-a-lesson-from-bee-colonies-7c5ffd0ba4c5?source=grid_home---------0------------------18%22}'
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
                        'path': '/s/story/to-make-your-business-more-efficient-take-a-lesson-from-bee-colonies-7c5ffd0ba4c5'
        }           
        
        
        
        
        
        medium=Medium(file_path)
        data=medium.getJsonResponse()
        #Check if the success Flag is True in the response
        is_success=medium.isRequestSuccess(data)
        has_reference_tag=medium.hasReferenceTag(data)
        postitem=PostsItem()
        tagitem=TagsItem()
        useritem=UserItem()
        collectionitem=CollectionItem()

        
        
        if is_success==True and has_reference_tag==True:
            data=data['payload']['references']
            if "Post" in data:
                posts=data["Post"]
                post_id=[]
                for post in posts:
                    post_id.append(post)
                    #print(post_id)
                for pid in post_id:
                    #postitem['postId']=posts[pid]['id']
                    #post_dict=medium.processPost(post[pid],postitem)
                    
                    postitem=medium.processPost(posts[pid],postitem)
                    postitem['searchTag']=response.meta['tag']
                    postitem['scrappedDate']=directory   
                    
                    uniqueSlug=postitem['uniqueSlug']
                    if uniqueSlug!='':
                        url="https://medium.com/s/story/"+uniqueSlug
                        yield scrapy.Request(url,method="GET",headers=header,cookies=cookie,callback=self.parse_story,meta={'id':pid,'folderpath':directory,'url':url,'tag':response.meta['tag']})
            # For each postId get the other fields from Json 
                    
                    yield postitem
                
                    post=posts[pid]
                    if 'virtuals' in post:
                        for tag in post['virtuals']['tags']:
                            tagitem=medium.processTags(tag,tagitem)
                            tagitem["scrappedDate"]=directory
                            yield tagitem
         
            ### Process User Information
            if 'User' in data:
                users=data['User']
                user_key=[]
                for user in users:
                    user_key.append(user)
                
                for key in user_key:
                    useritem=medium.processUsers(users[key],useritem)
                    useritem['scrappedDate']=directory
                    yield useritem
                    
            ### Process Publication Information
            
            if "Collection" in data:
                collections=data["Collection"]
                collections_key=[]
                for collection in collections:
                    collections_key.append(collection)
                
                for key in collections_key:
                    collectionitem=medium.processCollections(collections[key],collectionitem)
                    collectionitem['scrappedDate']=directory
                    yield collectionitem
            
        
        
        
        

                    
                    
        
        
        

    

