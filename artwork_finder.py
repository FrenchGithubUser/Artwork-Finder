import music_tag
from bing_image_downloader import downloader
import os
import sys


method = str(input("Download artworks from bing (b) or soundcloud (s) ? : "))

music_folder = "/home/gontran_macedoine/Documents/Projets python/Artwork_finder/music/"

musics = os.listdir(music_folder)

def download_album_art_bing():
	#prevents from printing useless stuff in the terminal
	sys.stdout = open(os.devnull, "w")
	downloader.download(music_name, limit=1,  output_dir='downloaded_artworks', adult_filter_off=True, force_replace=True)
	sys.stdout = sys.__stdout__

def download_album_art_soundcloud():
	#in developpement
	pass


def set_album_art():
	artwork_folder = f"./downloaded_artworks/{music_name}"
	
	files = os.listdir(artwork_folder)
	file = files[0]

	# set artwork
	with open(f"./downloaded_artworks/{music_name}/{file}", 'rb') as img_in:
	    f['artwork'] = img_in.read()
	with open(f"./downloaded_artworks/{music_name}/{file}", 'rb') as img_in:
	    f.append_tag('artwork', img_in.read())

	# Make a thumbnail (requires Pillow)
	#art.first.thumbnail([64, 64])  # -> pillow image
	#art.first.raw_thumbnail([64, 64])  # -> b'... raw thumbnail data ...'

	# finally, you can bounce the edits to disk
	f.save()


for music in musics:
	music_name = music.split(".", 1)[0]
	f = music_tag.load_file(f"{music_folder}{music}")
	try:
		test = f['artwork']
		print(f"{music_name} already has an artwork.")
	except:	
		print(f"{music_name} doesn't have any artwork. Adding one...")
		if method == "b":
			download_album_art_bing()
		elif method == "s":
			download_album_art_soundcloud()
		set_album_art()