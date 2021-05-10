from twitterapi import twitterdata
import pandas as pd
from pandasql import sqldf as sqlquery
from pytz import timezone
import streamlit as st

twitter = twitterdata()

def querygenerator(resource,place):
    tag1 = f'(#{resource.lower()} and #verified and #{place.lower()})'
    tag2 = f'(#{resource.lower()} and #verified)'
    tag3 = f'(#{resource.lower()} and #{place.lower()})'
    return [tag1,tag2,tag3]

@st.cache
def converttimezone(dateval):
    dateval = pd.to_datetime(dateval)
    return dateval.astimezone(tz=timezone('Asia/Kolkata'))

@st.cache(persist=True,show_spinner=False)
def searchresources(resource,place,hours):
    #query = f'#{resource.lower()} AND #verified AND #{place.lower()}' # and -is:retweet
    searchquery = querygenerator(resource,place)

    datalist = []
    for i in range(len(searchquery)):
        finalquery = searchquery[i]+' and -is:retweet'
        rawdata = twitter.gettweets(query=finalquery,max_results=60,hours=hours)
        tempdata = pd.DataFrame(rawdata,columns=rawdata.keys())
        tempdata['relevance'] = i+1
        datalist.append(tempdata)

    data = pd.concat(datalist,ignore_index=True)

    if len(data)>0:
        
        data[['name','username']] = pd.DataFrame(data.apply(lambda x: twitter.generateuserid(x['author_id']),axis=1).tolist(),index=data.index)
        data['created_at'] = data['created_at'].apply(converttimezone)
        
        data = sqlquery(
            '''
            Select distinct name,text,created_at,tweeturl from
            (
            select *,
            row_number() over (partition by text order by created_at) occurance_rank 
            from data 
            )k where occurance_rank = 1
            order by relevance,created_at desc
            '''
        )

    return data


