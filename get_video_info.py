#Get's video's likes, dislikes, views, and comments.

'''

SAMPLE JSON RESPONSE : 

{
 "kind": "youtube#videoListResponse",
 "etag": "\"xwzn9fn_LczrfK9QS3iZcGzqRGs/26m8nrWEf1a8GwB-k_maC929WPo\"",
 "pageInfo": {
  "totalResults": 1,
  "resultsPerPage": 1
 },
 "items": [
  {
   "kind": "youtube#video",
   "etag": "\"xwzn9fn_LczrfK9QS3iZcGzqRGs/KF9uTTwKyGREkIvmj3I8o8dijU0\"",
   "id": "Ks-_Mh1QhMc",
   "snippet": {
    "publishedAt": "2012-10-01T15:27:35.000Z",
    "channelId": "UCAuUUnT6oDeKwE6v1NGQxug",
    "title": "Your body language may shape who you are | Amy Cuddy",
    "description": "Body language affects how others see us, but it may also change how we see ourselves. Social psychologist Amy Cuddy argues that \"power posing\" -- standing in a posture of confidence, even when we don't feel confident -- can boost feelings of confidence, and might have an impact on our chances for success. (Note: Some of the findings presented in this talk have been referenced in an ongoing debate among social scientists about robustness and reproducibility. Read Amy Cuddy's response here: http://ideas.ted.com/inside-the-debate-about-power-posing-a-q-a-with-amy-cuddy/)\n\nGet TED Talks recommended just for you! Learn more at https://www.ted.com/signup.\n\nThe TED Talks channel features the best talks and performances from the TED Conference, where the world's leading thinkers and doers give the talk of their lives in 18 minutes (or less). Look for talks on Technology, Entertainment and Design -- plus science, business, global issues, the arts and more.\n\nFollow TED on Twitter: http://www.twitter.com/TEDTalks\nLike TED on Facebook: https://www.facebook.com/TED\n\nSubscribe to our channel: https://www.youtube.com/TED",
    "thumbnails": {
     "default": {
      "url": "https://i.ytimg.com/vi/Ks-_Mh1QhMc/default.jpg",
      "width": 120,
      "height": 90
     },
     "medium": {
      "url": "https://i.ytimg.com/vi/Ks-_Mh1QhMc/mqdefault.jpg",
      "width": 320,
      "height": 180
     },
     "high": {
      "url": "https://i.ytimg.com/vi/Ks-_Mh1QhMc/hqdefault.jpg",
      "width": 480,
      "height": 360
     },
     "standard": {
      "url": "https://i.ytimg.com/vi/Ks-_Mh1QhMc/sddefault.jpg",
      "width": 640,
      "height": 480
     },
     "maxres": {
      "url": "https://i.ytimg.com/vi/Ks-_Mh1QhMc/maxresdefault.jpg",
      "width": 1280,
      "height": 720
     }
    },
    "channelTitle": "TED",
    "tags": [
     "Amy Cuddy",
     "TED",
     "TEDTalk",
     "TEDTalks",
     "TED Talk",
     "TED Talks",
     "TEDGlobal",
     "brain",
     "business",
     "psychology",
     "self",
     "success"
    ],
    "categoryId": "22",
    "liveBroadcastContent": "none",
    "defaultLanguage": "en",
    "localized": {
     "title": "Your body language may shape who you are | Amy Cuddy",
     "description": "Body language affects how others see us, but it may also change how we see ourselves. Social psychologist Amy Cuddy argues that \"power posing\" -- standing in a posture of confidence, even when we don't feel confident -- can boost feelings of confidence, and might have an impact on our chances for success. (Note: Some of the findings presented in this talk have been referenced in an ongoing debate among social scientists about robustness and reproducibility. Read Amy Cuddy's response here: http://ideas.ted.com/inside-the-debate-about-power-posing-a-q-a-with-amy-cuddy/)\n\nGet TED Talks recommended just for you! Learn more at https://www.ted.com/signup.\n\nThe TED Talks channel features the best talks and performances from the TED Conference, where the world's leading thinkers and doers give the talk of their lives in 18 minutes (or less). Look for talks on Technology, Entertainment and Design -- plus science, business, global issues, the arts and more.\n\nFollow TED on Twitter: http://www.twitter.com/TEDTalks\nLike TED on Facebook: https://www.facebook.com/TED\n\nSubscribe to our channel: https://www.youtube.com/TED"
    },
    "defaultAudioLanguage": "en"
   },
   "statistics": {
    "viewCount": "17843575",
    "likeCount": "251916",
    "dislikeCount": "4971",
    "favoriteCount": "0",
    "commentCount": "8008"
   }
  }
 ]
}



'''


import os
import requests
import json
import urllib.parse


#VIDEO_ID = "fs_l_rovfBk" #Test video Teja Swaroop Channel
VIDEO_ID = os.getenv("VIDEO_ID")
API_KEY = os.getenv("API_KEY")
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def getinfo():
	resp = {}
	url = "https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet&id=%s&key=%s"%(VIDEO_ID,API_KEY)
	#urllib.parse.urlencode(url)

	headers = {
	"Accept" : 'application/json'
	}

	r = requests.get(url,headers=headers)
	j = json.loads(r.text)
	stats = j['items'][0]['statistics']
	title = j['items'][0]['snippet']['title']
	desc = j['items'][0]['snippet']['description']
	resp['title'] = title
	resp['description'] = desc
	resp['views'] = stats['viewCount']
	resp['likes'] = stats['likeCount']
	resp['dislikes'] = stats['dislikeCount']
	resp['comments'] = stats['commentCount']
	print(resp)
	return resp

if __name__=="__main__":
	getinfo()

#getinfo()


