import re
import json
import urllib.request
from pytube import YouTube
import sys

api_key = 'YOUR_API_KEY'    # enter your api key here

playlist = input("Enter the playlist link:\n")
playlist_id = re.split('list=', playlist)[1]

url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=25&playlistId={playlist_id}&key={api_key}'

json_url = urllib.request.urlopen(url)
data = json.loads(json_url.read())

while 1:
    try:
        token = data['nextPageToken']
        url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&pageToken={token}&playlistId={playlist_id}&key={api_key}'
        json_url = urllib.request.urlopen(url)
        temp = json.loads(json_url.read())
        data['items'].extend(temp['items'])
        data['nextPageToken'] = temp['nextPageToken']
    except:
        break

def exitDownloader():
    print("Thanks for using.\nMade with <3 by Anant Verma")
    sys.exit()
    
preference = int(input("Do you want automatic downloading of the best possible resolution for all the videos?(Press 1)\nOR\nDo you want to choose manually?(Press 2)\n"))
while preference != 1 and preference != 2 and preference != -1:
    preference = int(input("Invalid Input. Please enter 1 or 2 only (Enter -1 to exit): "))
subs_pref = 0

if preference== -1:
    exitDownloader()
    
elif preference == 1:
    subs_pref = int(input("Do you want to download English subs if available? (Press 1 for yes, 0 for no)\n"))
    while subs_pref != 1 and subs_pref != 0 and subs_pref != -1:
        subs_pref = int(input("Invalid Input. Please enter either 1 or 0 (Enter -1 to exit): "))

if subs_pref == -1:
    exitDownloader()

def select_available_options(video):   
    print("\nAvailaible option(s):")
    for i, value in enumerate(video.streams, start = 1):
        print(str(i) + ". " + value.type.capitalize() + " Format: ." + value.subtype + ", Resolution: " + str(value.resolution) + ", Size: " + str(round(value.filesize_approx/1048576,2)) + "MB")
    try:
        option = int(input("\nChoose the option you want (Press 0 to skip this video): "))
    except ValueError:
        option = int(input("Invalid Input. Please choose correct item number between {} and {}. Press 0 to skip, -1 to exit,\n\nChoose the option you want: ".format(1, len(video.streams))))
    
    while option < -1 or option > len(video.streams):
        option = int(input("Invalid Input. Please choose correct item number between {} and {}. Press 0 to skip, -1 to exit,\n\nChoose the option you want: ".format(1, len(video.streams))))
    return option
    
def getVideoTitle(i, data):
    title = str(i+1) + ". " + data['items'][i]['snippet']['title']
    return title

def getVideoLink(i, data):
    link = "https://www.youtube.com/watch?v=" + data['items'][i]['snippet']['resourceId']['videoId']
    return link

def downloadVideo(video, itag):
    print("\nDownloading: " + '" '+ title + "." + video.streams.get_by_itag(itag).subtype + '"'+ " ...")
    video.streams.get_by_itag(itag).download(filename = title)
    print("Download completed.\n")
    
def select_Subtitle(caps):
    print("Subtitles are available for the video in the following languages.")
    caps_list = list(caps.lang_code_index.values())
    for i, sub in enumerate(caps_list,  start = 1):
        print(str(i) + ". " + sub.name)
    subs_option = int(input("Enter the item number to download that subtitle otherwise, press 0: "))
    while subs_option < -1 or subs_option > len(caps):
            subs_option = int(input("Invalid Input. Please choose correct item number between {} and {}.\n\nChoose the option you want: ".format(1, len(caps))))
    return subs_option

def downloadSubs(caps, lang_code):
    caps[lang_code].download(title = title)
    print("\nSubtitles downloaded.\n")
    
for i in range(len(data['items'])):
    title = getVideoTitle(i, data)
    video_link = getVideoLink(i, data)

    print("\n\nVideo Name: " + title)

    video = YouTube(video_link)
    if preference == 1:
        itag = video.streams.get_highest_resolution().itag
    elif preference == 2:
        option = select_available_options(video)
    
        if option == 0:
            continue
        elif option == -1:
            exitDownloader()
        itag = video.streams[option-1].itag
    
    downloadVideo(video, itag)
    
    caps = video.captions
    if(len(caps) >=1):
        if subs_pref == 0:
            subs_option = select_Subtitle(caps)
            if subs_option == 0:
                continue
            elif subs_option == -1:
                exitDownloader()
            lang_code = list(caps.lang_code_index.values())[subs_option-1].code
        elif subs_pref == 1:
            lang_code = "en"
        downloadSubs(caps, lang_code)
    print("-"*50)
print("Thanks for using.\nMade with <3 by Anant Verma")
sys.exit()