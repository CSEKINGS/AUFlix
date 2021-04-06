import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
import pprint
import pyrebase
from collections import defaultdict

# Firebase configuration
config = {
        'apiKey': "AIzaSyB2jAveBDZ6m8YBKEh1iCP2xJLLSeFoYyA",
        'authDomain': "auflix-67633.firebaseapp.com",
        'databaseURL': "https://auflix-67633-default-rtdb.firebaseio.com",
        'projectId': "auflix-67633",
        'storageBucket': "auflix-67633.appspot.com",
        'messagingSenderId': "757795130164",
        'appId': "1:757795130164:web:d2dd6d191911a0a7977361"
}

# Extract playlist id from url
def Yscrap():
    firebase=pyrebase.initialize_app(config)
    
    # DB initialization
    db=firebase.database()
    urls = ['https://www.youtube.com/playlist?list=PLOgMKE5DWMGLEoAqF4K5yn_OlKN9lE-I7']
    for url in urls:
        query = parse_qs(urlparse(url).query, keep_blank_values=True)
        playlist_id = query["list"][0]
        # print(f'get all playlist items links from {playlist_id}')
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = "AIzaSyApozlICeSR0LPn-twRy6Od6YNfjzNHwRI")
        request = youtube.playlistItems().list(part = "snippet",playlistId = playlist_id,)
        response = request.execute()

        playlist_items = []
        while request is not None:
            response = request.execute()
            playlist_items += response["items"]
            request = youtube.playlistItems().list_next(request, response)
        d=defaultdict(dict)
        for p in playlist_items:
            d[p["snippet"]["resourceId"]["videoId"]]={'id':p["snippet"]["resourceId"]["videoId"],'title':p['snippet']['title'],'description':p['snippet']['description'],'publishat':p['snippet']['publishedAt']}
        # pprint.pprint(d)

        # Set to the firebase db
        db.child('test').set(d)