# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

'''
Created by Aiswarya : 19 Oct 2018
scrapy crawl -a start_date=20170901 -a end_date=20180930 -a tagSlug='data-science' -o "data_science//medium_scrapper_%(item_name)s.csv" -t csv  medium_scrapper 


'''

import scrapy



class PostsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    postId=scrapy.Field()
    creatorId=scrapy.Field()
    createdAt=scrapy.Field()
    firstPublishedAt=scrapy.Field()
    latestPublishedAt=scrapy.Field()
    updatedAt=scrapy.Field()
    imageCount=scrapy.Field()
    linksCount=scrapy.Field()
    readingTime=scrapy.Field()
    recommends=scrapy.Field()
    responsesCreatedCount=scrapy.Field()
    socialRecommendsCount=scrapy.Field()
    tagsCount=scrapy.Field()
    wordCount=scrapy.Field()
    title=scrapy.Field()
    subTitle=scrapy.Field()
    searchTag=scrapy.Field()
    collectionId=scrapy.Field()
    totalClapCount=scrapy.Field()
    isSubscriptionLocked=scrapy.Field()
    tags_name=scrapy.Field()
    uniqueSlug=scrapy.Field()
    inReponseToPostId=scrapy.Field()
    audioVersionDurationSec=scrapy.Field()
    scrappedDate=scrapy.Field()
    vote=scrapy.Field() # Have I Bookmarked this page??
    language=scrapy.Field()
    text=scrapy.Field()
    #pass

class TagsItem(scrapy.Item):
    slug=scrapy.Field()
    name=scrapy.Field()
    postCount=scrapy.Field()
    scrappedDate=scrapy.Field()
    followerCount=scrapy.Field()

class UserItem(scrapy.Item):
    userId=scrapy.Field()
    userName=scrapy.Field()
    author=scrapy.Field()
    createdAt=scrapy.Field()
    bio=scrapy.Field()
    scrappedDate=scrapy.Field()

class CollectionItem(scrapy.Item):
    collectionId=scrapy.Field()
    name=scrapy.Field()
    slug=scrapy.Field()
    description=scrapy.Field()
    followerCount=scrapy.Field()
    publicEmail=scrapy.Field()
    facebookPageName=scrapy.Field()
    twitterUsername=scrapy.Field()
    domain=scrapy.Field()
    tags=scrapy.Field() # These are the tags associated with a publication
    scrappedDate=scrapy.Field()

class ContentItem(scrapy.Item):
    postId=scrapy.Field()
    userId=scrapy.Field()
    usersFollowedCount=scrapy.Field()
    usersFollowedByCount=scrapy.Field()
    text=scrapy.Field()
    scrappedDate=scrapy.Field()
    url=scrapy.Field()
    
    
    
    
