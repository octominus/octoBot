import urllib3
import urllib.request
import requests
from bs4 import BeautifulSoup

def download_xkcd_images():
    error = 0
    imageNumber = 0
    while(not error):
        url = "https://xkcd.com/" + str(imageNumber) + "/"
        r = requests.get(url)
        content = r.content
        soup = BeautifulSoup(content, "html.parser")

        errorCheck = soup.findAll('h1')

        if len(errorCheck) == 0:
            image = soup.findAll('img')[2]
            # ! Her zaman görsel 2 bizim için gerçek görsel
            link = url + image["src"]
            folderLink = "pics/xkcd/img"+str(imageNumber)+".jpg"
            downloadText = "Downloaded img" + str(imageNumber) +".jpg from --> " + link
            urllib.request.urlretrieve(link, folderLink)
            print(downloadText)
            imageNumber = imageNumber + 1
        else:
            print("Error! Stop script!")
            error = 1

download_xkcd_images()




"""
import random as rn

def file_len(filename):
    count = 0
    file = open(filename, "r", encoding="utf8")
    for line in file:
        if line != "\n":
            count = count + 1
    file.close()
    return count

def rand_line_select(filename):
    file = open(filename, "r", encoding="utf8")
    jokeNumber = rn.randint(1, file_len(filename))
    count = 0
    for line in file:
        if line != "\n":
            count = count + 1
        if count == jokeNumber:
            file.close()
            return line

print(rand_line_select("jokes/saka.txt"))
"""