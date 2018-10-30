import datetime
import codecs
import os
import json
from medium.items import PostsItem,TagsItem,UserItem,CollectionItem,ContentItem


class Medium:
    
    def __init__(self,fileName):
        self.fileName=fileName
        #self.data=getJsonResponse()
    def hasBodyModelParaTag(self,data):
        if isRequestSuccess(self,data) and  hasValueTag(self,data)==True:
            if "content" in data['payload']['value']:
                if 'bodyModel' in data['payload']['value']['content']:
                    if 'paragraphs' in data['payload']['value']['content']['bodyModel']:
                        return True
        return False      
    
    def getJsonResponse(self):
        with codecs.open(self.fileName,'r','utf-8') as infile:
            data=json.load(infile)
        return data
    
    def isRequestSuccess(self,data):
        if "success" in data:
            if data['success']==True:
                return True
        return False 
    
    def hasPayload(self,data):
        if "payload" in data:
            return True
        else:
            return False  
    def hasReferenceTag(self,data):
        
        if 'payload' in data:
            if 'references' in data['payload']:
                return True
        return False
    def hasValueTag(self,data):
        
        if hasPayload(self,data)==True:
            data=data["payload"]
            if "value" in data:
                return True
        return False    
    

    
    def hasSocialStats(self,data):
        if isRequestSuccess(self,data) and hasReferenceTag(self,data):
            if "SocialStats" in data['payload']['references']:
                return True
            else:
                return False
    
    def processContent(self,data,contentitem):
        
        text=""
        try:
            data_content=data['payload']['value']['content']['bodyModel']['paragraphs']
            for content in data_content:
                try:
                    text=text+content['text']+"\n"
                except:
                    text=text
        except:
            text=""
        
        contentitem['text']=text
        ## Get the user related measure - get only the first user data
        if "SocialStats" in data['payload']['references']:
            user_key=[]
            for index,user in enumerate(data['payload']['references']['SocialStats']):
                if index==0:
                    user_key.append(user)
        for key in user_key:
            contentitem['usersFollowedCount']=data['payload']['references']['SocialStats'][key]['usersFollowedCount']
            contentitem['usersFollowedByCount']=data['payload']['references']['SocialStats'][key]['usersFollowedByCount']
        
                
        
             
        
        return contentitem
        
        
    def processCollections(self,collection,collectionitem):
        collectionitem['collectionId']=collection['id']
        collectionitem['name']=collection['name']
        collectionitem['slug']=collection['slug']
        collectionitem['description']=collection['description']
        if 'metadata' in collection:
            followerCount=collection['metadata']['followerCount']
        try:
            collectionitem['publicEmail']=collection['publicEmail']
        except:
            collectionitem['publicEmail']=""
        try:
            collectionitem["facebookPageName"]=collection["facebookPageName"]
        except:
            collectionitem["facebookPageName"]=""
        try:
            collectionitem["twitterUsername"]=collection["twitterUsername"]
        except:
            collectionitem["twitterUsername"]=""
        try:
            collectionitem["domain"]=collection['domain']
        except:
            collectionitem["domain"]=""
        try:
            collectionitem["tags"]=",".join(collection["tags"])
        except:
            collectionitem["tags"]=""
            
        return collectionitem
    
    def processUsers(self,user,useritem):
        useritem["userId"]=user["userId"]
        useritem["userName"]=user["username"]
        useritem["author"]=user["name"]
        
        useritem["createdAt"]=user["createdAt"]
        useritem["bio"]=user["bio"]     
        
        return useritem
    
    def processTags(self,tag,tagItem):
        tagItem['slug']=tag['slug']
        tagItem['name']=tag['name']
        try:
            tagItem["postCount"]=tag['metadata']["postCount"]
        except:
            tagItem["postCount"]=0        
            
        if 'metadata' in tag and 'followerCount' in tag['metadata']:
            tagItem["followerCount"]=tag['metadata']["followerCount"]
            
            #tagItem['scrappedDate']=scrappedDate            
        return tagItem
    
    def processPost(self,post,postItem):
        postItem['postId']=post['id']
        postItem['creatorId']=post['creatorId']
        postItem['createdAt']=str(post['createdAt'])
        postItem['firstPublishedAt']=str(post['firstPublishedAt'])
        postItem['latestPublishedAt']=str(post['latestPublishedAt'])
        postItem['updatedAt']=str(post['updatedAt'])
        postItem['vote']=post['vote']
        postItem['language']=post['detectedLanguage']
        postItem['title']=post['title']
        
        
        postItem['collectionId']=post["homeCollectionId"]
        
        postItem['isSubscriptionLocked']=post['isSubscriptionLocked']
        
        postItem['uniqueSlug']=post['uniqueSlug']
        postItem['inReponseToPostId']=post['inResponseToPostId']
        postItem['audioVersionDurationSec']=post["audioVersionDurationSec"]
        
        if 'virtuals' in post:
            virtuals=post['virtuals']
            
            try:
                postItem['imageCount']=virtuals['imageCount']
            except:
                postItem['imageCount']=0
            try:
                postItem['linksCount']=len(virtuals["links"]["entries"])
            except:
                postItem['linksCount']=0
            
            postItem['readingTime']=virtuals['readingTime']
            postItem['recommends']=virtuals['recommends']
        
            postItem['responsesCreatedCount']=virtuals['responsesCreatedCount']
            
            postItem['tagsCount']=len(virtuals["tags"])
            
            postItem['wordCount']=virtuals["wordCount"]
            
            postItem['totalClapCount']=virtuals["totalClapCount"]
            
            postItem['socialRecommendsCount']=virtuals['socialRecommendsCount']
            
            postItem['subTitle']=virtuals['subtitle']
          
            tag_list=[]
            for tag in virtuals['tags']:
                
                tag_list.append(tag['name'])
                
                    
                    
        postItem['tags_name']=",".join(tag_list)    
        
        
        return postItem
    
        
    

        
    
    
        
    





