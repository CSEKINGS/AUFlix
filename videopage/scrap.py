import googleapiclient.discovery
import pprint
import pyrebase
import json
import nltk
import requests
import re
import numpy as np
from urllib.parse import parse_qs, urlparse
from collections import defaultdict
from datetime import datetime
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup
nltk.download('stopwords')

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
        self.vurls = [
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
        self.nurls = urls = [
            "https://padeepz.net/civil-engineering-syllabus-notes-important-questions-and-question-bank/",
            "https://padeepz.net/anna-university-mechanical-engineering-syllabus-notes-important-questions-and-question-bank/",
            "https://padeepz.net/anna-university-electrical-and-electronics-engineering-eee-syllabus-notes-important-questions-and-question-bank/",
            "https://padeepz.net/anna-university-electronics-and-communication-engineering-ece-syllabus-notes-important-questions-and-question-bank/",
            "https://padeepz.net/anna-university-computer-science-and-engineering-cse-syllabus-notes-important-questions-and-question-bank/",
        ]
        self.d = defaultdict(dict)

    def Yscrap(self):  # Extract playlist id from url
        for url in self.vurls:
            query = parse_qs(
                urlparse("https://www.youtube.com/playlist?list=" + url).query,
                keep_blank_values=True,
            )
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
        self.db.child("videos").set(self.tagger(self.d))  # Set to the firebase db

    def tagger(self, d):
        for k in d.keys():
            keys = []
            for k2 in d[k].keys():
                d[k][k2]["keys"] = self.keygen(
                    " ".join([d[k][k2]["title"], d[k][k2]["description"]])
                )
                d[k][k2]["keys"]=[ky for ky in list(set(d[k][k2]["keys"])) if not ky.isdigit()]
                for kw in d[k][k2]["keys"]:keys.append(kw)
            d[k]['title']=d[k][k2]["description"]
            d[k]["keys"] = list(set(keys))
        return d

    def keygen(self, wl):
        keys = []
        # ps = PorterStemmer()
        stopWord = list(set(stopwords.words("english")))
        stopWord.append('tutor')
        stopWord.append('video')
        stopWord.append('test')
        stopWord.append('pratical')
        stopWord.append('example')
        for word in RegexpTokenizer(r"\w+").tokenize(wl.lower()):
            if word not in stopWord:keys.append(word)
        return keys

    def Nscrap(self): # Notes link scrapper
        d = defaultdict(dict)
        reg = r"^https://padeepz.(net|com)/.*notes.*"
        for url in self.nurls:
            for ptag in BeautifulSoup(requests.get(url).content, "html5lib").findAll(
                "p"
            ):
                for link in ptag.findAll("a", href=re.compile(reg)):
                    d[url.replace("https://padeepz.net/", "").replace("/", "")][
                        link["href"]
                        .replace("https://padeepz.net/", "")
                        .replace("/", "")
                    ] = []
                    for ptag1 in BeautifulSoup(
                        requests.get(link["href"]).content, "html5lib"
                    ).findAll("p"):
                        for link1 in ptag1.findAll("a", href=re.compile(reg)):
                            for dlink in BeautifulSoup(
                                requests.get(link1["href"]).content, "html5lib"
                            ).findAll("a", href=re.compile(r"^https://drive.*")):
                                d[
                                    url.replace("https://padeepz.net/", "").replace(
                                        "/", ""
                                    )
                                ][
                                    link["href"]
                                    .replace("https://padeepz.net/", "")
                                    .replace("/", "")
                                ].append(
                                    [
                                        link1["href"]
                                        .replace("https://padeepz.net/", "")
                                        .replace("/", ""),
                                        dlink["href"].replace("https://drive.google.com/open?id=",""),
                                        self.keygen(
                                            link["href"]
                                            .replace("https://padeepz.net/", "")
                                            .replace("/", "")
                                        ),
                                    ]
                                )
        self.db.child("notes").set(d)

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

# requests==2.11.1
# Pyrebase==3.0.27
# google-api-core==1.26.3
# appdirs==1.4.4
# asgiref==3.3.2
# beautifulsoup4==4.9.3
# bs4==0.0.1
# cachetools==4.2.1
# certifi==2020.12.5
# chardet==4.0.0
# click==7.1.2
# Django==3.2
# gcloud==0.17.0
# google-api-core
# google-api-python-client==2.1.0
# google-auth==1.28.0
# google-auth-httplib2==0.1.0
# googleapis-common-protos==1.53.0
# html5lib==1.1
# httplib2==0.19.1
# idna==2.10
# joblib==1.0.1
# jws==0.1.3
# mypy-extensions==0.4.3
# nltk==3.6.1
# numpy==1.20.2
# oauth2client==3.0.0
# packaging==20.9
# pathspec==0.8.1
# protobuf==3.15.7
# pyasn1==0.4.8
# pyasn1-modules==0.2.8
# pycryptodome==3.4.3
# pyparsing==2.4.7
# Pyrebase
# python-jwt==2.0.1
# pytz==2021.1
# regex==2021.4.4
# requests
# requests-toolbelt==0.7.0
# rsa==4.7.2
# six==1.15.0
# soupsieve==2.2.1
# sqlparse==0.4.1
# toml==0.10.2
# tqdm==4.60.0
# typed-ast==1.4.2
# typing-extensions==3.7.4.3
# uritemplate==3.0.1
# urllib3==1.26.4
# webencodings==0.5.1
