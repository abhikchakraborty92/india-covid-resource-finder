from twitterapi import twitterdata
import pandas as pd
from pandasql import sqldf as query
from pytz import timezone
import streamlit as st

twitter = twitterdata()

# def taggenerator(resource,place):
#     return f'%23{resource.lower()} and %23verified and %23{place.lower()}'

@st.cache
def converttimezone(dateval):
    dateval = pd.to_datetime(dateval)
    return dateval.astimezone(tz=timezone('Asia/Kolkata'))

@st.cache(persist=True)
def searchresources(resource,place,hours):
    tag = f'#{resource.lower()} and #verified and #{place.lower()} and -is:retweet'

    rawdata = twitter.gettweets(tag,max_results=40,hours=hours)
    data = pd.DataFrame(rawdata,columns=rawdata.keys())

    if len(data)>0:

        data[['name','username']] = pd.DataFrame(data.apply(lambda x: twitter.generateuserid(x['author_id']),axis=1).tolist(),index=data.index)
        data['created_at'] = data['created_at'].apply(converttimezone)

        data = query(
            '''
            Select name,text,created_at,tweeturl from
            (
            select *,
            row_number() over (partition by text order by created_at) occurance_rank 
            from data 
            )k where occurance_rank = 1
            order by created_at desc
            '''
        )

    return data


