import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
import pprint
import pyrebase
from collections import defaultdict
import json
import nltk
import numpy as np
from datetime import datetime
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

class AUSCRAPER:
    def __init__(self):
        # nltk.download()
        config = {  # Firebase configuration
            "apiKey": "AIzaSyB2jAveBDZ6m8YBKEh1iCP2xJLLSeFoYyA",
            "authDomain": "auflix-67633.firebaseapp.com",
            "databaseURL": "https://auflix-67633-default-rtdb.firebaseio.com",
            "projectId": "auflix-67633",
            "storageBucket": "auflix-67633.appspot.com",
            "messagingSenderId": "757795130164",
            "appId": "1:757795130164:web:d2dd6d191911a0a7977361",
        }
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()  # DB initialization
        self.urls = [
            "PLOgMKE5DWMGI2aI6Vur33LxVuoL0Aun0k",
            "PLOgMKE5DWMGK6bfWjEHg97E1x3fJramhJ",
            "PLOgMKE5DWMGIBRctaUdXgwORzqqdloiHt",
            "PLOgMKE5DWMGJrahAQzYDHUEbOpDvZoAv3",
            "PLOgMKE5DWMGLEoAqF4K5yn_OlKN9lE-I7",
            "PLOgMKE5DWMGJksPaR9DGkI0LgQcYWNtou",
            "PLOgMKE5DWMGJ2ePXlONTn5BxrXY7yMH6c",
            "PLOgMKE5DWMGLrGkIB9Pi3BHbTxcdgEXHJ",
            "PLOgMKE5DWMGImSgdSqix5iA6khdzoImzJ",
            "PLOgMKE5DWMGKFNfN2TwKjLNgTMuZdFN6A",
            "PLOgMKE5DWMGLZ8LF8uY4ujDHXIqlViDlR",
            "PLOgMKE5DWMGKkVM16aJbk-RnC2NVnvj4H",
            "PLOgMKE5DWMGIKMJzqieg98q2u4fgczh9P",
            "PLOgMKE5DWMGKKDLeY2v-CiSXafu0hg9h7",
            "PLOgMKE5DWMGJBAFSLTyu4NtXUXGpG85bR",
            "PLOgMKE5DWMGKyGTFU7eRwHi_wci02slXn",
            "PLOgMKE5DWMGJUbP6vOLxhGEbvrWeDdh3c",
            "PLOgMKE5DWMGLPENN4_LXmp-ZzAidbuwVX",
            "PLOgMKE5DWMGK_7CoUikPty9f--gjQjuWw",
            "PLOgMKE5DWMGKDhiuxN3LSNF8Kq6ORzzWO",
            "PLOgMKE5DWMGJW_4NU2iT1W9ZQsVfS0h4s",
            "PLOgMKE5DWMGLOGqqzN2YXFGM_0jdDffpS",
            "PLOgMKE5DWMGKQLI41sc_kaAKVj3qAnMCW",
            "PLOgMKE5DWMGK32dScH2-Kc4pCQMFHhyVk",
            "PLOgMKE5DWMGK2seIWUzQaZdVt9nQqjbAB",
            "PLOgMKE5DWMGJtUMDPYFBKv8kI8OcTq-ep",
            "PLOgMKE5DWMGLZcBxYJBFAikdhAaAXJ1_U",
            "PLOgMKE5DWMGKy1uomFjd9__LnVj-DFbWm",
            "PLOgMKE5DWMGKhi0RYaiCTwOYaCh20iNZZ",
        ]
        self.d = defaultdict(dict)

    def Yscrap(self):  # Extract playlist id from url
        for url in self.urls:
            query = parse_qs(urlparse("https://www.youtube.com/playlist?list="+url).query, keep_blank_values=True)
            playlist_id = query["list"][0]
            # print(f'get all playlist items links from {playlist_id}')
            youtube = googleapiclient.discovery.build(
                "youtube", "v3", developerKey="AIzaSyApozlICeSR0LPn-twRy6Od6YNfjzNHwRI"
            )
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
            )
            response = request.execute()

            playlist_items = []
            while request is not None:
                response = request.execute()
                playlist_items += response["items"]
                request = youtube.playlistItems().list_next(request, response)
            for p in playlist_items:
                self.d[url][p["snippet"]["resourceId"]["videoId"]] = {
                    "id": p["snippet"]["resourceId"]["videoId"],
                    "title": p["snippet"]["title"],
                    "description": p["snippet"]["description"],
                    "publishat": p["snippet"]["publishedAt"],
                }
        self.d=self.tagger(self.d)
        # pprint.pprint(self.d)
        # self.d['date']=int(datetime.now().strftime('%j'))
        self.db.child("videos").set(self.d) # Set to the firebase db

    def tagger(self, d):
        for k in d.keys():
            keys = []
            for k2 in d[k].keys():
                d[k][k2]["stopwords"], d[k][k2]["keys"] = self.keygen(
                    " ".join([d[k][k2]["title"], d[k][k2]["description"]])
                )
                for kw in d[k][k2]["keys"]:
                    keys.append(kw)
            d[k]["keys"] = list(set(keys))
        return d

    def keygen(self, wl):
        keys = []
        sw = []
        ps = PorterStemmer()
        stopWord = set(stopwords.words("english"))
        for word in RegexpTokenizer(r"\w+").tokenize(wl.lower()):
            if word in stopWord:
                sw.append(word)
            else:
                keys.append(ps.stem(word))
        return list(set(sw)), list(set(keys))

    # def matcher(self,str1,str2):
    #         size_x=len(str1)+1
    #         size_y=len(str2)+1
    #         m=np.zeros((size_x,size_y))
    #         for x in range(size_x):m[x,0]=x
    #         for y in range(size_y):m[0,y]=y
    #         for x in range(1,size_x):
    #             for y in range(1,size_y):
    #                 if str1[x-1]==str2[y-1]:m[x,y]=m[x-1,y-1]
    #                 else:m[x,y]=min(m[x-1,y]+1,m[x-1,y-1],m[x,y-1]+1)
    #         return 1-(m[size_x-1,size_y-1]/size_x)
