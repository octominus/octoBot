import random as rn
from click import pass_context
import discord
from discord import voice_client
from discord import channel
from discord.ext import commands
import os

from discord.utils import get

with open('token.txt', 'r') as f: TOKEN = f.read()

# ! Random muzik kodlari
# comicFileNumber = len(os.listdir("pics/xkcd"))

musicFolder = "music"
musicFile = ""
musicFolderFile = ""
musicFiles = os.listdir(musicFolder)
musicFileNumber = len(musicFiles)

def randMusic():
    randomMusicNumber = rn.randint(0, musicFileNumber-1)
    randomMusic = musicFiles[randomMusicNumber]
    music = musicFolder + "/" + randomMusic
    return music, randomMusic

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix = 'o.', intents= intents)  # starts the discord client.

@client.event  # event decorator/wrapper. More on decorators here: https://pythonprogramming.net/decorators-intermediate-python-tutorial/
async def on_ready():  # method expected by client. This runs once when connected
    print(f'We have logged in as {client.user}')  # notification of login.

@client.command(pass_contect = True)
async def join(ctx):
    voice_channel = ctx.author.voice.channel
    await voice_channel.connect()
    await ctx.message.channel.send("```I am back bitchezzzzzzz!!!!!! ^^```")

@client.command(pass_contect = True)
async def leave(ctx):
    guild = ctx.guild
    bot_voice_channel = client.voice_clients
    voice_client: discord.VoiceClient = discord.utils.get(bot_voice_channel, guild = guild)
    await voice_client.disconnect()
    await ctx.message.channel.send("```octoBot disconnected -_-```")

@client.command(aliases = ['music', 'listen'])
async def play(ctx, *args):
    emptyArg = ()
    if args == emptyArg:
        guild = ctx.guild
        bot_voice_channel = client.voice_clients
        voice_client: discord.VoiceClient = discord.utils.get(bot_voice_channel, guild = guild)
        musicFolderFile, musicFile = randMusic()
        audio = discord.FFmpegPCMAudio(musicFolderFile)
        if not voice_client.is_playing():
            await ctx.message.channel.send(f"```♪♫ Now Playing ♪♫\n-[{musicFile}]```")
            voice_client.play(audio, after=None)
    else:
        if args[0] == 'list':
            await ctx.message.channel.send(f"```Second Word: {args[0]}```")
            musicList = "```♪♫ Current Music List ♪♫\n"
            index = 1
            for musicName in musicFiles:
                musicList = musicList + f"{index} - " + musicName + "\n"
                index = index + 1 
            musicList = musicList + "```"
            await ctx.message.channel.send(musicList)
        else:
            listNumber = int(args[0]) - 1
            await ctx.message.channel.send(f"```Selected Music: {listNumber+1} - {musicFiles[listNumber]}```")
            guild = ctx.guild
            bot_voice_channel = client.voice_clients
            voice_client: discord.VoiceClient = discord.utils.get(bot_voice_channel, guild = guild)
            audio = discord.FFmpegPCMAudio(f"sounds/music/{musicFiles[listNumber]}")
            if voice_client.is_playing():
                await ctx.message.channel.send(f"```♪♫ Now Playing ♪♫\n-[{musicFiles[listNumber]}]```")
                voice_client.stop()
                voice_client.play(audio, after=None)

@client.command(pass_contect = True)
async def next(ctx):
    guild = ctx.guild
    bot_voice_channel = client.voice_clients
    voice_client: discord.VoiceClient = discord.utils.get(bot_voice_channel, guild = guild)
    if voice_client.is_playing():
        voice_client.stop()
    musicFolderFile, musicFile = randMusic()
    audio = discord.FFmpegPCMAudio(musicFolderFile)
    if not voice_client.is_playing():
        await ctx.message.channel.send(f"```♪♫ Now Playing ♪♫\n-[{musicFile}]```")
        voice_client.play(audio, after=None)

@client.command(pass_contect = True)
async def pause(ctx):
    guild = ctx.guild
    bot_voice_channel = client.voice_clients
    voice_client: discord.VoiceClient = discord.utils.get(bot_voice_channel, guild = guild)

    if voice_client.is_playing():
        await ctx.message.channel.send(f"```♪♫ Paused - [{sound_path}]```")
        voice_client.pause()

@client.command(pass_contect = True)
async def stop(ctx):
    guild = ctx.guild
    bot_voice_channel = client.voice_clients
    voice_client: discord.VoiceClient = discord.utils.get(bot_voice_channel, guild = guild)

    if voice_client.is_playing():
        await ctx.message.channel.send(f"```♪♫ Stoped - [{sound_path}]```")
        voice_client.stop()

@client.command(pass_contect = True)
async def version(ctx):
    latestUpdateNotes = "Upgraded music playing function. Music lovers can show music list and listen whatever they want in this list. Fuck man this is so funny. #_#"
    latestVersion = "1.0.3"
    await ctx.send(f"```Version: {latestVersion}\n\nLatest Patch Notes:\n{latestUpdateNotes}```")

@client.command(pass_contect = True)
async def info(ctx):
    createdBy = "octominus#4447"
    latestVersion = "1.0.3"
    embed = discord.Embed(title=f"octoBot v{latestVersion}", colour=0x87CEEB)
    embed.add_field(name=f"Created by {createdBy}", value=None, inline=False)
    embed.add_field(name="Server ", value=ctx.message.guild.name, inline=True)
    embed.add_field(name="Server Owner", value=ctx.message.guild.owner, inline=True)
    embed.add_field(name="Server Creation Date", value=ctx.message.guild.created_at, inline=True)
    await ctx.send(embed=embed)

@client.command(pass_context = True)
async def feature(ctx, *args):
    emptyArg = ()
    if args == emptyArg:
        embed = discord.Embed(colour=0xb042f5)
        embed.add_field(name="add function", value="You can give an advice for developer with using 'o.feature add' command", inline=False)
        embed.add_field(name="list function", value="You can list features with 'o.feature list' command")
        await ctx.send(embed=embed)
    else:
        f = open("features.txt", "r+")
        FEATURE_TEXT = f.read()

        if args[0] == 'add':
            print('added')

        elif args[0] == 'list':
            if FEATURE_TEXT == "":
                await ctx.send("No any feature!")
            else:
                embed = discord.Embed(colour=0xf542dd)
                embed.add_field(name="list of features", value=f"{FEATURE_TEXT}")
                await ctx.send(embed=embed)
            print('listed')

        f.close()

@client.command(pass_contect = True)
async def debug(ctx):
    text = "Debug Mode Not Using Now"
    await ctx.message.channel.send(text)

@client.command(pass_contect = True)
async def octo(ctx):
    await ctx.send(f"I miss you honey :(")
    

client.run(TOKEN)  # recall my token was saved!
