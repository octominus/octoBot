import random as rn
import os

musicFolder = "sounds/music"
musicFiles = os.listdir(musicFolder)
musicFileNumber = len(musicFiles)

def randMusic():
    randomMusicNumber = rn.randint(1, musicFileNumber)
    nowPlayinMusic = musicFiles[randomMusicNumber]
    musicFileName = musicFolder + "/" + nowPlayinMusic
    print(musicFileName)

randMusic()