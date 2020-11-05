import music_tag
from bing_image_downloader import downloader
import os
import sys
import time
from selenium import webdriver
import wget
import requests


method = str(input("Download artworks from bing (b) or soundcloud (sc) or shazam (sh) ? : "))

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

def download_album_art_shazam():
	fp = webdriver.FirefoxProfile()

	driver = webdriver.Firefox(fp)
	url = 'https://www.shazam.com/'
	#opens firefox and goes to the url
	driver.get(url)


	#avoids getting an error because the page didn't fully load (find_element_by_xpath & click)
	def febx_click(xpath):
	        try:
	                driver.find_element_by_xpath(xpath).click()
	        except:
	                time.sleep(0.5)
	                febx_click(xpath)

	#avoids getting an error because the page didn't fully load (find_element_by_xpath & sends a string)
	def febx_keys(xpath, keys):
	        try:
	                driver.find_element_by_xpath(xpath).send_keys(keys)
	        except:
	                time.sleep(0.5)
	                febx_keys(xpath, keys)

	#finds all the images in the webpage and returns the artwork
	def find_artwork():
	        while True:
	                images = driver.find_elements_by_tag_name('img')
	                
	                if len(images)<=4: #when not all the images are loaded
	                	time.sleep(0.5)
	                	images = driver.find_elements_by_tag_name('img')				
	                 
	                else:
	                    break

	        for elt in images:
	                image_url = elt.get_attribute('src')
	                if 'coverart' in image_url:
	                        break
	        return image_url


	#finds the search bar and clicks on it
	febx_click('//*[@id="search-input"]')
	#find the search bar and writes the music name
	febx_keys('//*[@id="search-input"]', music_name)
	#clicks on the search button
	febx_click('//*[@id="/search/header"]/div/form/button')
	#clicks on the first music found
	time.sleep(5)
	
	febx_click('/html/body/div[5]/div/div/div[2]/div/div[2]/ul[1]/li[1]')
		
	artwork_url = find_artwork()

	r = requests.get(artwork_url)

	path = os.path.join('./downloaded_artworks', f'{music_name}')
	os.mkdir(path) 
	with open(f"./downloaded_artworks/{music_name}/{music_name}_artwork.jpg", "wb") as f:
	    f.write(r.content)

	driver.quit() 


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
		elif method == "sc":
			download_album_art_soundcloud()
		elif method == "sh":
			download_album_art_shazam()
		set_album_art()
