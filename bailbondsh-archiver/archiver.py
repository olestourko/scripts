from __future__ import print_function
import sys
import subprocess
import argparse
import json

parser = argparse.ArgumentParser(description="Archives prank callsh from youtube.")
parser.add_argument("file", help="A file with a lost of youtube channels.")
parser.add_argument("path", help="The base path where videos will be archived.")
parser.add_argument("-r", "--limit-rate", dest="limit_rate", help="Maximum download rate in bytes per second(e.g. 50K or 4.2M)")
args = parser.parse_args()

if subprocess.call(["which", "youtube-dl"]) == 0:
	f = open(args.file, 'r')
	channels = json.loads(f.read())
	base_path = args.path if args.path.endswith("/") else args.path + "/"

	for key, url in channels.items():
		call = ["youtube-dl", "--simulate", "-o", base_path + '%(uploader)s/%(title)s-%(id)s', url]
		if args.limit_rate:
			call.extend(["--limit-rate", args.limit_rate])
		
		subprocess.call(call)

else:
	print("youtube-dl not found.", file=sys.stderr)
	exit(1)
