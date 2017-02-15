from __future__ import print_function
import sys
import subprocess
import argparse
import json

parser = argparse.ArgumentParser(description="Archives prank callsh from youtube.")
parser.add_argument("file", help="A file with a lost of youtube channels.")
parser.add_argument("path", help="The base path where videos will be archived.")
parser.add_argument("-r", "--limit-rate", dest="limit_rate", help="Maximum download rate in bytes per second(e.g. 50K or 4.2M)")
parser.add_argument("-a", "--audio-only", dest="audio_only", help="Archives only the audio.", action="store_true")
args = parser.parse_args()

if subprocess.call(["which", "youtube-dl"]) == 0:
	f = open(args.file, 'r')
	channels = json.loads(f.read())
	base_path = args.path if args.path.endswith("/") else args.path + "/"
	base_call = ["youtube-dl"]
	
	if args.limit_rate:
		base_call = base_call.extend(["--limit-rate", args.limit_rate])
		
	for key, url in channels.items():
		if args.audio_only:
			call = list(base_call)
			call.extend(["-o", base_path + '%(uploader)s/%(title)s-%(id)s.%(ext)s', url, "--extract-audio", "--audio-quality", "3", "--audio-format", "m4a", "--embed-thumbnail"])
			subprocess.call(call)
		else:
			call = list(base_call)
			call.extend(["-o", base_path + '%(uploader)s/%(title)s-%(id)s', url])
			subprocess.call(call)

else:
	print("youtube-dl not found.", file=sys.stderr)
	exit(1)
