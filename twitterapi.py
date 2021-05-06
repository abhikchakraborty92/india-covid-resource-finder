import requests
import json
import datetime
import os

class twitterdata:
    
    def __creds(self):
        apikey = os.environ.get('apikey')
        apisecret = os.environ.get('apisecret')
        return apikey, apisecret

    def generatetoken(self):

        tokenrequest = json.loads(requests.post(self.access_token_url,auth=(self.apikey,self.apisecret)).text)
        return tokenrequest.get('access_token')
    
    def __init__(self):
        cred = self.__creds()
        self.apikey = cred[0]
        self.apisecret = cred[1]
        self.access_token_url = 'https://api.twitter.com/oauth2/token?grant_type=client_credentials'
        self.access_token = self.generatetoken()

    def __generateheader(self,token):
        return {"authorization": f"Bearer {token}"}

    def generateuserid(self,userid):
        url = f"https://api.twitter.com/2/users/{userid}"
        
        headers = self.__generateheader(self.access_token)
        # params = {
        #     "id":userid
        # }
        user = requests.get(url, headers=headers)
        if user.status_code == 401:
            self.access_token = self.generatetoken()
            headers = self.__generateheader(self.access_token)
            user = requests.get(url, headers=headers)
        
        if user.status_code == 200:
            user = json.loads(user.text).get('data')
        else:
            print(user.text)
            return 'UnknownUser','UnknownUsername'
        
        return user.get('name','UnknownUser'),user.get('username','UnknownUsername')

    
    def __parsetweets(self,tweetbody):
        data = {
            "id":[],
            "author_id":[],
            "text":[],
            "created_at":[],
            "tweeturl":[]
        }
        tweetbody = json.loads(tweetbody).get('data',[])

        if len(tweetbody)>0:
            for item in tweetbody:      
                data.get('id').append(item.get('id'))
                data.get('author_id').append(item.get('author_id'))
                data.get("text").append(item.get('text'))
                data.get("created_at").append(item.get('created_at'))
                data.get("tweeturl").append(f"https://twitter.com/anyuser/status/{item.get('id')}")
        

        return data
    
    def generatestarttime(self,hours):
        starttime = datetime.datetime.utcnow() - datetime.timedelta(hours=hours)
        return starttime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
    def generateparams(self,max_results,hashtag,tweetfields,starttime,next_token = None):
        params = {
            'max_results' : max_results,
            'query' : hashtag,
            'tweet.fields' : tweetfields,
            'start_time':starttime
        }
        if next_token:
            params['next_token']=next_token
        
        return params


    def gettweets(self,hashtag,hours,max_results=100,next_token=None):
        #hashtag = hashtag.replace('#','%23')
        starttime = self.generatestarttime(hours)
        parameters = self.generateparams(max_results,hashtag,'source,created_at,attachments,author_id',starttime,next_token=next_token)
        
        #url = f"https://api.twitter.com/2/tweets/search/recent?max_results={max_results}&query={hashtag}&tweet.fields=source,created_at,attachments,author_id&start_time={starttime}"
        url = 'https://api.twitter.com/2/tweets/search/recent'
        headers = self.__generateheader(self.access_token)
        tweetresponse = requests.get(url, headers=headers,params=parameters)

        if tweetresponse.status_code == 401:
            self.access_token = self.generatetoken()
            headers = self.__generateheader(self.access_token)
            tweetresponse = requests.get(url, headers=headers,params=parameters)
        
        if tweetresponse.status_code == 200:
            tweetdata = self.__parsetweets(tweetresponse.text)
        else:
            tweetdata = {}
        
        return tweetdata