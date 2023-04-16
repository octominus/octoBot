import requests
import base64
import asyncio
import os
import logging

#import spotifyConfigSet as spotifyConfig
import spotifyConfig

import discord
from discord.ext import commands

# ? Discord bot settings
with open('token.txt', 'r') as f: TOKEN = f.read()
intents = discord.Intents.default()
intents.message_content = True      
octoBot = commands.Bot(command_prefix = 'o.', intents = intents)

# ? Logging settings
FORMAT = '%(asctime)s \033[94m%(levelname)s\033[0m %(funcName)8s(): %(message)s'
logging.basicConfig(format = FORMAT, level = logging.INFO)

# ? Set up the Spotify API client
SPOTIPY_CLIENT_ID=spotifyConfig.SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET=spotifyConfig.SPOTIPY_CLIENT_SECRET

# ! Get a Spotify access token using the client ID and client secret
def get_spotify_access_token():
    auth_header = base64.b64encode((SPOTIPY_CLIENT_ID + ':' + SPOTIPY_CLIENT_SECRET).encode('ascii')).decode('ascii')
    headers = {'Authorization': 'Basic %s' % auth_header}
    data = {'grant_type': 'client_credentials'}
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    return response.json()['access_token']

# ! Search for a track on Spotify and return the track ID and preview URL
def search_spotify_track(query, access_token):
    headers = {'Authorization': 'Bearer %s' % access_token}
    params = {'q': query, 'type': 'track'}
    response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
    track = response.json()['tracks']['items'][0]
    track_id = track['id']
    track_name = track['name']
    track_image = track['album']['images'][0]['url']
    artist_name = track['artists'][0]['name']
    return track_id, track_name, artist_name, track_image

# ! Download the audio data for a track from its preview URL
def download_track_audio(track_name, artist_name):
    search_query = f"{track_name} {artist_name} official audio"
    search_url = f"https://www.youtube.com/results?search_query={search_query}"
    response = requests.get(search_url)
    # extract video ID from search result page
    try:
        video_id = None
        for line in response.text.splitlines():
            if "watch?v=" in line:
                video_id = line.split("watch?v=")[1].split('"')[0]
                print("video_id", video_id)
                break
        if video_id is None:
            raise Exception("Could not extract video ID from search results.")
    except Exception as e:
        print(f"Error: {e}")
        exit()
    # download the audio from the youtube video
    try:
        output_file = f"music/{artist_name}/{track_name}"
        music_file = f"{output_file}.mp3"
        if not os.path.exists(music_file):
            os.system(f'youtube-dl --extract-audio --audio-format mp3 --audio-quality 0 --output "{output_file}.%(ext)s"  https://www.youtube.com/watch?v={video_id}')
        return music_file

    except Exception as e:
        print(f"Error downloading audio: {e}")
        exit()

# ! Bot Events
@octoBot.event
async def on_ready():
    print(f'{octoBot.user} has connected to Discord!')

async def connect_to_voice_channel(ctx):
    if ctx.voice_client:
        await ctx.voice_client.move_to(ctx.author.voice.channel)
        voice_client = ctx.voice_client
    else:
        # Connect bot to user's voice channel
        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()
    return voice_client

async def track_info_publishers(ctx, artist_name, track_name, track_image):
    embed = discord.Embed(title=f"{track_name}", colour=0x87CEEB).set_thumbnail(url=track_image)
    embed.add_field(name=f"{artist_name}", value="", inline=False)
    await ctx.send(embed=embed)

@octoBot.command()
async def play(ctx, *args):
    access_token = get_spotify_access_token()
    track_info = " ".join(args)
    track_id, track_name, artist_name, track_image = search_spotify_track(track_info, access_token)

    music_file = download_track_audio(track_name, artist_name)

    logging.info(f"Track ID: {track_id}")
    logging.info(f"Track name: {track_name}")
    logging.info(f"Track image URL: {track_image}")
    logging.info(f"Artist name: {artist_name}")
    logging.info(f"Music file name: {music_file}")

    voice_channel = ctx.author.voice.channel
    channel_connection = asyncio.create_task(connect_to_voice_channel(ctx))
    voice_client = await channel_connection

    if voice_channel:
        if not voice_client.is_playing():
            audio = discord.FFmpegPCMAudio(f"{music_file}")
            voice_client.play(audio, after=None)
            asyncio.create_task(track_info_publishers(ctx, artist_name, track_name, track_image))
        else:
            voice_client.stop()
            await ctx.message.channel.send(f"```♪♫ Now Playing ♪♫\n-[{artist_name} - {track_name}]```")
            audio = discord.FFmpegPCMAudio(f"{music_file}")
            voice_client.play(audio, after=None)
    else:
        await ctx.channel.send('You must be in a voice channel to play music')
        return
    
    # # Wait for the audio to finish playing before disconnecting
    # while voice_client.is_playing():
    #     await asyncio.sleep(1)

    # await voice_client.disconnect()

# @octoBot.command(pass_contect = True)
# async def stop(ctx):
#     # Stop the current playback
#     sp.pause_playback()
#     await ctx.send("Playback stopped.")

# @octoBot.command(pass_contect = True)
# async def pause(ctx):
#     # Pause the current playback
#     sp.pause_playback()
#     await ctx.send("Playback paused.")

# @octoBot.command(pass_contect = True)
# async def resume(ctx):
#     # Resume the current playback
#     sp.start_playback()
#     await ctx.send("Playback resumed.")

# @octoBot.command(pass_contect = True)
# async def skip(ctx):
#     # Skip to the next track
#     sp.next_track()
#     await ctx.send("Skipping to the next track.")

octoBot.run(TOKEN)