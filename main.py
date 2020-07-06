import re
import json
import urllib.request
from pytube import YouTube

api_key = 'Your_API_Key'    # enter your api key here

playlist = input("Enter the playlist link")
playlist_id = re.split('list=', playlist)[1]

url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=25&playlistId={playlist_id}&key={api_key}'
json_url = urllib.request.urlopen(url)
data = json.loads(json_url.read())



def available_options(yt):
    for i, value in enumerate(yt.streams, start = 1):
        print(str(i) + ". " + value.type.capitalize() + " Format: ." + value.subtype + ", Resolution: " + str(value.resolution) + ", Size: " + str(round(value.filesize_approx/1048576,2)) + "MB")

def getVideoTitle(i, data):
    title = i + ". " + data['items'][i]['snippet']['title']
    return title
def getVideoLink(i, data):
    link = "https://www.youtube.com/watch?v=" + data['items'][i]['snippet']['resourceId']['videoId']
    return link


for i in range(len(data['items'])):
    title = getVideoTitle(i, data)
    video_link = getVideoLink(i, data)
    print(title)
    print("\nAvailaible options:")
    yt = YouTube(video_link)
    available_options(yt)
    o = int(input("\nChoose the option you want: "))
    while o <= 0 or o > len(yt.streams):
        o = int(input("Invalid Input. Please choose correct item number between {} and {}.\n\nChoose the option you want: ".format(1, len(yt.streams))))
    print("\nDownloading: " + title + "...")
    yt.streams[o-1].download(filename = title)
    print("Download completed.\n")