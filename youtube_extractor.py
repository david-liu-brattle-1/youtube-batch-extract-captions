#! python3

import youtube_dl
import os
import ujson as json
import re

ydl = youtube_dl.YoutubeDL({'writeautomaticsub':True, 'subtitleslangs':['en'],'skip_download':True, 'max_downloads':100,
                            'format':'worstvideo'})
yt = ydl.get_info_extractor('Youtube')
yts = ydl.get_info_extractor('YoutubeSearch')
yt_playlist = ydl.get_info_extractor('YoutubePlaylist')

def get_playlist(user):
    if not os.path.exists(user+'.txt'):
        video_list = yt_playlist._extract_playlist(user)
        video_list = list(res[1]['entries'])
    else:
        video_list = json.loads(open(user + '.txt').read())

def download_captions(video_list):
    for i in video_list:
        filename = f"out/{i['title'].replace('/','')}-{i['id']}.vtt".replace(':','').replace('?','')
        if not os.path.exists(filename):
            print(i['title'])
            video_id = i['id']
            url = 'http://www.youtube.com/watch?v=%s&gl=US&hl=en&has_verified=1&bpctr=9999999999' % video_id
            video_webpage = yt._download_webpage(url, video_id)
            ac = yt.extract_automatic_captions(video_id,video_webpage)
            if not ac:
                print("ERROR")
                open(filename,'w').write('')
                continue
            url = None
            for j in ac['en']:
                if j['ext']=='vtt':
                    url=j['url']
                    break

            sub = yt._request_webpage(url, video_id, note=False).read().decode()
            sub = re.sub('<.*?>','',sub)#.replace(' align:start position:19%','')
            open(filename,'w').write(sub)

if __name__ == '__main__':
    user = 'UU3tNpTOHsTnkmbwztCs30sA'    

    video_list = get_playlist(user)
    open(user + '.txt','w').write(json.dumps(video_list))

    download_captions(video_list)
