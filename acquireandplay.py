from __future__ import unicode_literals
import argparse
import os

parser = argparse.ArgumentParser(description='video to screen.')
parser.add_argument('id', metavar='N', type=str,
                    help='yt id')

args = parser.parse_args()


import youtube_dl

if not os.path.exists(args.id + ".mp3"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': args.id + '.mp3'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['http://www.youtube.com/watch?v=' + args.id])
else:
    print("already dl'd")


if not os.path.exists(args.id + ".wav"):
    os.system("ffmpeg -i " + args.id + ".mp3 " + args.id + ".wav")
else:
    print("alr conv")

if not os.path.exists(args.id + ".json"):
    #put your conversion code here
else:
    print("already chord json")

if not os.path.exists(args.id + ".json" + ".chords.lrc"):
    #and here
else:
    print("already lrc'd")

os.system("py ./player.py " + args.id + ".json.chords.lrc" + " " + args.id + ".wav")
