# ! Bir dosyada toplam satır sayısını hesaplama
def file_len(filename):
    count = 0
    file = open(filename, "r", encoding="utf8")
    for line in file:
        if line != "\n":
            count = count + 1
    file.close()
    return count

# ! Random şaka kodları
def randJoke(filename):
    file = open(filename, "r", encoding="utf8")
    jokeNumber = rn.randint(1, file_len(filename))
    count = 0
    for line in file:
        if line != "\n":
            count = count + 1
        if count == jokeNumber:
            file.close()
            return line

# ! Egometre kodu
def egoMeter(username):
    if username == "octominus#4447":
        return "Gereksiz egolu"
    else:
        return rn.randint(10, 90)

#@client.event
#async def on_message(message):  # event that happens per any message.
#
#    # each message has a bunch of attributes. Here are a few.
#    # check out more by print(dir(message)) for example.
#
#    serverID = client.get_guild(550406162592301066)
#    callStatus = 0
#
#    if str(message.content) == "octo.ego" in message.content.lower():
#        await message.channel.send(ego)
#    
#    if str(message.content) == "octo.meme" in message.content.lower():
#        imageNumber = rn.randint(1,5)
#        imageName = "pics/meme/meme" + str(imageNumber) + ".jpg"
#        await message.channel.send(file=discord.File(imageName))
#
#    if str(message.content) == "octo.comic" in message.content.lower():
#        comicNumber = rn.randint(0,comicFileNumber-1)
#        comicName = "pics/xkcd/img" + str(comicNumber) + ".jpg"
#        await message.channel.send(file=discord.File(comicName))
#
#    if str(message.content) == "octo.joke" in message.content.lower():
#        joke = randJoke("jokes/saka.txt")
#        await message.channel.send(joke)
#
#    if str(message.content) == "octo.server":
#        serverInfo = f"```Number of members: {serverID.member_count}```"
#        await message.channel.send(serverInfo)
#
#    if str(message.content) == "octo.help":
#        serverInfo = "..."
#        await message.channel.send(serverInfo)
#
#    if str(message.content) == "octoBot":
#        await message.channel.send("Efendim, canım!")
#        callStatus = 1
#
#    if str(message.content) == "Nasılsın":
#        await message.channel.send("Seninle beraber olduğum sürece her zaman iyiyim <3")
#        callStatus = 0