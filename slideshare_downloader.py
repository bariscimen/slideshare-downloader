#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import img2pdf
import re
from os import listdir, walk
from os.path import isfile, join
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
from slugify import slugify
import shutil
from tqdm import tqdm

CURRENT = os.getcwd()

def download(url):
	rgx = re.compile(r"-(\d*)-1024\.jpg")

	html = urlopen(url).read()
	soup = BeautifulSoup(html, "html.parser")
	folder = 'pdf_images' #soup.title.string
	images = soup.findAll('img', {'class':'slide_image'})
	os.mkdir(folder)

	file_list = []
	for image in tqdm(images):
	    image_url = image.get('data-full').split('?')[0]
	    num = rgx.findall(image_url)[0]
	    file_list.append(num)
	    urlretrieve(image_url, folder + "/" + num + ".jpg")


	f = ["%s/%s.jpg" % (folder, x) for x in file_list]

	pdf_bytes = img2pdf.convert(f, dpi=300, x=None, y=None)
	slug = slugify(soup.find("span", {'class': 'j-title-breadcrumb'}).text.strip())
	doc = open(slug + '.pdf', 'wb')
	doc.write(pdf_bytes)
	doc.close()

	shutil.rmtree(folder)

	print("Saved as %s.pdf" % (slug,))

if __name__ == "__main__":
    url = input('Slideshare URL : ')
    download(url)
