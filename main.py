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

print("\n\nEnter -1 at any input stage to abort further downloading.")

def select_available_options(video):   
    print("\nAvailaible option(s):")
    for i, value in enumerate(video.streams, start = 1):
        print(str(i) + ". " + value.type.capitalize() + " Format: ." + value.subtype + ", Resolution: " + str(value.resolution) + ", Size: " + str(round(value.filesize_approx/1048576,2)) + "MB")
    option = int(input("\nChoose the option you want (Press 0 to skip this video): "))
    while option < -1 or option > len(video.streams):
        option = int(input("Invalid Input. Please choose correct item number between {} and {}. Press 0 to skip, -1 to exit,\n\nChoose the option you want: ".format(1, len(video.streams))))
    return option
    
def getVideoTitle(i, data):
    title = str(i+1) + ". " + data['items'][i]['snippet']['title']
    return title

def getVideoLink(i, data):
    link = "https://www.youtube.com/watch?v=" + data['items'][i]['snippet']['resourceId']['videoId']
    return link

def downloadVideo(video, option):
    print("\nDownloading: " + '" '+ title + "." + video.streams[option-1].subtype + '"'+ " ...")
    video.streams[option-1].download(filename = title)
    print("Download completed.\n")
    
def select_Subtitle(caps):
    print("Subtitles are available for the video in the following languages.")
    caps_list = list(caps.lang_code_index.values())
    for i, sub in enumerate(caps_list,  start = 1):
        print(str(i) + ". " + sub.name)
    subs_option = int(input("Enter the item number to download that subtitle otherwise, press 0: "))
    while subs_option < -1 or subs_option > len(caps):
            subs_option = int(input("Invalid Input. Please choose correct item number between {} and {}. Press 0 to skip, -1 to exit,\n\nChoose the option you want: ".format(1, len(caps))))
    return subs_option

def downloadSubs(caps, option):
    list(caps.lang_code_index.values())[subs_option-1].download(title = title)
    print("\nDownload completed.\n")
    
for i in range(len(data['items'])):
    title = getVideoTitle(i, data)
    video_link = getVideoLink(i, data)

    print("\n\nVideo Name: " + title)

    video = YouTube(video_link)
    option = select_available_options(video)
    
    if option == 0:
        continue
    elif option == -1:
        print("Exiting..\nThanks for using,\nMade with <3 by Anant Verma")
        sys.exit()
    else:
        downloadVideo(video, option)

    caps = video.captions
    if(len(caps) >=1):
        subs_option = select_Subtitle(caps)
        if subs_option == 0:
            pass
        elif subs_option == -1:
            print("Thanks for using,\nMade with <3 by Anant Verma")
            sys.exit()
        else:
            downloadSubs(caps, option)
    print("-"*50)