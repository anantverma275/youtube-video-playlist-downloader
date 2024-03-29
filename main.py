import re
import json
import urllib.request
from pytube import YouTube
import sys

api_key = 'AIzaSyBM2C6EmXIeKcXrU1GdU3uq7M8qMQVoulg'    # enter your api key here
answer = int(input("What do you want to download?\n1.Video\n2.Playlist\n"))

def exitDownloader():
    print("Thanks for using.\nMade with <3 by Anant Verma")
    sys.exit()
    
while answer != 1 and answer !=2 and answer != -1:
    answer = int(input("Invalid input. Press 1 for Video, 2 for Playlist (Enter -1 to exit): "))
if answer == -1:
    exitDownloader()
elif answer == 1:
    video = input("Enter the video link:\n")
    try:
        video_id = video.split("watch?v=")[1].split("&")[0]
    except:
        video_id = video.split("be/")[1]
    url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}'
    json_url = urllib.request.urlopen(url)
    data = json.loads(json_url.read())
    length = 1

elif answer == 2:
    playlist = input("Enter the playlist link:\n")
    playlist_id = re.split('list=', playlist)[1]
    
    url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=25&playlistId={playlist_id}&key={api_key}'
    
    json_url = urllib.request.urlopen(url)
    data = json.loads(json_url.read())
    length = len(data['items'])

while 1:
    try:
        token = data['nextPageToken']
        url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&pageToken={token}&playlistId={playlist_id}&key={api_key}'
        json_url = urllib.request.urlopen(url)
        temp = json.loads(json_url.read())
        data['items'].extend(temp['items'])
        data['nextPageToken'] = temp['nextPageToken']
    except:
        length = len(data['items'])
        break

#options to download all, specific videos, range of videos
op = 0
if answer == 2:
    while 1:
        op = int(input(
            "Do you want to download all(0) or specific videos(1) or a range of videos from start index to end index(2)?"))
        if op != 0 and op != 1 and op != 2:
            continue
        else:
            break

    if op == 0:
        pass

    elif op == 1:
        while 1:
            indices = list(map(int, input(
                f"Enter the indices of the video you want to download starting from 1 to {length}").split()))
            if max(indices) > length or min(indices) < 1:
                print("Please enter valid indices\n")
                continue
            else:
                break

    elif op == 2:
        while 1:
            try:
                start, end = map(int, input(
                    f"Enter start, end index (default: 1, {length}):\n").split())
            except ValueError:
                print("Please enter valid value for both start and end")
                continue
            if start <= end and start >= 1 and end <= length:
                break
            else:
                print("Please enter valid value for both start and end")
                pass

preference = int(input(
    "Do you want automatic downloading of the best possible resolution?(Press 1)\nOR\nDo you want to choose manually?(Press 2)\n"))
while preference != 1 and preference != 2 and preference != -1:
    preference = int(
        input("Invalid Input. Please enter 1 or 2 only (Enter -1 to exit): "))
subs_pref = 0

if preference == -1:
    exitDownloader()

elif preference == 1 and answer == 2:
    subs_pref = int(input(
        "Do you want to download English subs if available? (Press 1 for yes, 0 for no)\n"))
    while subs_pref != 1 and subs_pref != 0 and subs_pref != -1:
        subs_pref = int(
            input("Invalid Input. Please enter either 1 or 0 (Enter -1 to exit): "))

if subs_pref == -1:
    exitDownloader()


def getVideoStreams(video):
    video_streams = []
    for stream in video.streams:
        if stream.audio_codec:
            video_streams.append(stream)
    return video_streams


def select_available_options(streams):
    print("\nAvailaible option(s):")
    for i, stream in enumerate(streams, start=1):
        print(str(i) + ". " + stream.type.capitalize() + " Format: ." + stream.subtype + ", Resolution: " +
              str(stream.resolution) + ", Size: " + str(round(stream.filesize_approx/1048576, 2)) + "MB")
    option = int(
        input("\nChoose the option you want (Press 0 to skip this video): "))
    while option < -1 or option > len(streams):
        option = int(input("Invalid Input. Please choose correct item number between {} and {}. Press 0 to skip, -1 to exit,\n\nChoose the option you want: ".format(1, len(streams))))
    return option


def getVideoTitle(i, data):
    if answer == 1:
        title = data['items'][i]['snippet']['title']
    elif answer == 2:
        title = str(i+1) + ". " + data['items'][i]['snippet']['title']
    return title


def getVideoLink(i, data):
    pre = "https://www.youtube.com/watch?v="
    if answer == 1:
        link = pre + video_id
    else:
        link = pre + data['items'][i]['snippet']['resourceId']['videoId']
    return link


def downloadVideo(video, itag):
    print("\nDownloading: " + '"' + title + "." +
          video.streams.get_by_itag(itag).subtype + '"' + " ...")
    video.streams.get_by_itag(itag).download(filename=title)
    print("Download completed.\n")


def select_Subtitle(caps):
    print("Subtitles are available for the video in the following languages.")
    caps_list = list(caps.lang_code_index.values())
    for i, sub in enumerate(caps_list,  start=1):
        print(str(i) + ". " + sub.name)
    subs_option = int(
        input("Enter the item number to download that subtitle otherwise, press 0: "))
    while subs_option < -1 or subs_option > len(caps):
        subs_option = int(input(
            "Invalid Input. Please choose correct item number between {} and {}.\n\nChoose the option you want: ".format(1, len(caps))))
    return subs_option


def downloadSubs(caps, lang_code):
    caps[lang_code].download(title=title)
    print("\nSubtitles downloaded.\n")


for i in range(length):
    if op == 1:
        if len(indices) == 0:
            break
        if i+1 in indices:
            indices.remove(i+1)
        else:
            continue
    elif op == 2:
        if i + 1 < start:
            print(str(i))
            continue
        elif i == end:
            print(str(i))
            break
    title = getVideoTitle(i, data)
    video_link = getVideoLink(i, data)
    print("Video link to submit: " + video_link)
    print("\nConnecting...")
    video = YouTube(video_link)
    print("\n\nConnected.\nVideo Name: " + title)
    video_streams = getVideoStreams(video)
    if preference == 1:
        print("\n\nFinding the best quality")
        itag = video.streams.get_highest_resolution().itag
    elif preference == 2:
        option = select_available_options(video_streams)

        if option == 0:
            continue
        elif option == -1:
            exitDownloader()
        itag = video_streams[option-1].itag

    downloadVideo(video, itag)

    caps = video.captions
    if(len(caps) >= 1):
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
