#!/usr/bin/env python3
import json
import os
from twython import Twython
from urllib.request import urlretrieve as download

#Change to script's directory
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

#Import config
from config import (
    API_KEY, API_SECRET, TOKEN, TOKEN_SECRET
)

#Authentication
bot = Twython(API_KEY, API_SECRET, TOKEN, TOKEN_SECRET)


#Get status
status = (bot.get_user_timeline(user_id='2196922086', count=1)) #This id is the ID of @OnePlus, change if needed
tweet = status[0]
dump = json.dumps(tweet)
js = json.loads(dump)
tweetID = js['id_str']

#Make sure tweet is new
try:
    with open('./.lasttweet.txt') as f:
        lastTweet = f.read()
    if lastTweet == tweetID:
        print("No new tweets; exiting...")
        quit()

except FileNotFoundError:
    print(".lasttweet.txt not found; creating file and continuing...")
    open('.lasttweet.txt', 'a').close()

#Check if tweet is a reply
if js['in_reply_to_status_id'] != None:
    print("Tweet is a reply, exiting...")
    quit()
#Check if tweet is a retweet
try:
    if js['retweeted_status']:
        print("Tweet is a retweet; exiting...")
        quit()
except KeyError:
    pass


#Get text from tweet
text = js['text']

#Check if there are URLS in the tweet
if js['entities']['urls']:
    print("Tweet contains URLs.")
    text = text.replace(js['entities']['urls'][0]['url'], js['entities']['urls'][0]['display_url']) #Change t.co url into display url, to actually mirror the tweet
    print(text + '(replaced with actual url)')

#Check if media is present in tweet
try:
    mediaType = (js['extended_entities']['media'][0]['type'])
    print("Media is a(n) " + mediaType)
    isMedia = True
    if mediaType == "photo": #Download image to flip it and reupload it
        i = 0
        for m in js['extended_entities']['media']:
            download(js['extended_entities']['media'][i]['media_url_https'], "image{}".format(str(i)))
            print(mediaType + str(i) + " downloaded, flipping image...")
            os.system("convert ./image{0} -rotate 180 ./image{0}.png && rm ./image{0}".format(str(i)))
            text = text.replace(js['extended_entities']['media'][i]['url'], "")
            i += 1

    elif mediaType == "animated_gif" or mediaType == "video": #Download and flip video
        def downloadVideo(i):
            downloaded = False
            while downloaded is False:
                url = js['extended_entities']['media'][0]['video_info']['variants'][i]['url']
                if url.endswith('.mp4'):
                    download(url, 'video.mp4')
                    downloaded = True
                else:
                    i += 1
        downloadVideo(0)
        print(mediaType + " downloaded, flipping video...")
        os.system("ffmpeg -i video.mp4 -vf 'transpose=2,transpose=2' output.mp4") #https://stackoverflow.com/a/9570992/8225853
        text = text.replace(js['extended_entities']['media'][0]['url'], "")

except KeyError:
    print("No media in tweet; continuing...")


#List of chars + their flipped counterpart
chars = "abcdefghijklmnpqrtuvwxyzABCDEFGHIJKLMNPQRTUVWYZ12345679!?&*(),.'🙂👍👎_/\\" #https://github.com/appu1232/Discord-Selfbot/blob/master/cogs/fun.py#L129
fchars = "ɐqɔpǝɟƃɥᴉɾʞlɯudbɹʇnʌʍxʎz∀qƆpƎℲפHIſʞ˥WNԀQɹ┴∩ΛM⅄ZƖᄅƐㄣϛ9ㄥ6¡¿⅋*)('˙,🙃👎👍‾\\/"
flip = {}


#Put each char with its inverted counterpart in the same list
for n, c in enumerate(chars):
    flip[c] = fchars[n]

#Flip!
output = ""
for c in text:
    if c in flip:
        output += flip[c]
    else:
        output += c
output = "@oneplus " + output[::-1] #Defaults to the oneplus twitter account, change if needed

#Reply to tweet
if isMedia is True:
    if mediaType == 'photo':
        media_files = []
        uploaded_media = []

        for f in os.listdir(path):
            if 'image' in f:
                media_files.append(f)

        for f in media_files:
            with open(f, 'rb') as image:
                response = bot.upload_media(media=image)
                uploaded_media.append(response['media_id'])

        bot.update_status(status=output, in_reply_to_status_id=tweetID, media_ids=uploaded_media)

    elif mediaType == 'animated_gif' or mediaType == 'video':
        with open('./output.mp4', 'rb') as video:
            response = bot.upload_video(media=video, media_type='video/mp4')
        bot.update_status(status=output, in_reply_to_status_id=tweetID, media_ids=[response['media_id']])

else:
    bot.update_status(status=output, in_reply_to_status_id=tweetID)

#Write tweet ID to .lasttweet.txt
print("Writing tweet id to ./.lasttweet.txt ...")
with open('./.lasttweet.txt', 'w') as f:
    f.write(tweetID)

#Cleanup files
print("Cleaning up...")
extensions = ['.png', '.mp4']
for f in os.listdir(path):
   if f.endswith(tuple(extensions)):
        os.remove(f)

print("Done.")
