from __future__ import print_function
import os
import subprocess

#todo: read channels from a file
urls = [
	"https://www.youtube.com/channel/UCC9jQr2TF_tz75WoXxYH27Q" #Carlos Walnut
]

if not subprocess.call(["which", "youtube-dl"]):
	print("youtube-dl found. Ready to go!")
	for url in urls:
		subprocess.call(["youtube-dl", "-o", '%(uploader)s/%(title)s-%(id)s', url])

else:
	print("youtube-dl not found.")
