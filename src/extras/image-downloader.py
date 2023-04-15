"""import urllib3
import urllib.request
import requests
from bs4 import BeautifulSoup

def download_xkcd_images():
    error = 0
    imageNumber = 2199
    emptyImage = 3
    while(not error):
        url = "https://xkcd.com/" + str(imageNumber) + "/"
        r = requests.get(url)
        content = r.content
        soup = BeautifulSoup(content, "html.parser")

        errorCheck = soup.findAll('h1')
        imageCheck = "//imgs.xkcd.com/comics/"
        if len(errorCheck) == 0:
            images = soup.findAll('img')
            for image in images:
                if image["src"][0:len(imageCheck)] == imageCheck:
                    link = url + image["src"]
                    folderLink = "pics/xkcd/img"+str(imageNumber-3-emptyImage)+".jpg"
                    downloadText = "Downloaded img" + str(imageNumber) +".jpg from --> " + link

                    urllib.request.urlretrieve(link, folderLink)
                    print(downloadText)
                    imageNumber = imageNumber + 1
        else:
            print("Error! Stop script!")
            error = 1

download_xkcd_images()
"""



for pos in range(len(files)):
    filename = "img"+str(pos)+".jpg"
    os.rename("pics/xkcd/"+files[pos], filename) 
    print(pos)
