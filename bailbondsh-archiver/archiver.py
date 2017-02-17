from __future__ import print_function
import sys
import subprocess
import argparse
import json

parser = argparse.ArgumentParser(description="Archives prank callsh from youtube.")
parser.add_argument("file", help="A file with a lost of youtube channels.")
parser.add_argument("path", help="The base path where videos will be archived.")
parser.add_argument("-r", "--limit-rate", dest="limit_rate", help="Maximum download rate in bytes per second(e.g. 50K or 4.2M)")
parser.add_argument("-a", "--audio", dest="get_audio", help="Also download a seperate audio file along with the video.", action="store_true")
args = parser.parse_args()

if subprocess.call(["which", "youtube-dl"]) == 0:
	f = open(args.file, 'r')
	channels = json.loads(f.read())
	base_path = args.path if args.path.endswith("/") else args.path + "/"

        base_call = ["youtube-dl"]
        if args.limit_rate:
                base_call = base_call.extend(["--limit-rate", args.limit_rate])

	for key, url in channels.items():
                call = list(base_call)
                call.extend(["-o", base_path + '%(uploader)s/%(title)s-%(id)s', url])

                #download videos
		#subprocess.call(call)

                #also download the audio files, if the flag is set
                if args.get_audio:
                    call = list(base_call)
                    call.extend(["-o", base_path + '%(uploader)s/audio_only/%(title)s-%(id)s', url, "--extract-audio", "--audio-quality", "3"])
                    subprocess.call(call)

else:
	print("youtube-dl not found.", file=sys.stderr)
	exit(1)
