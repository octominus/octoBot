import wave
import discord
from discord.ext import commands
import wavelink

with open('token.txt', 'r') as f: TOKEN = f.read()

intents = discord.Intents.default()
octoBot = commands.Bot(command_prefix = '$', intents = intents)

wavelink.Player

@octoBot.event
async def on_ready():
    print(f'We have logged in as {octoBot.user}')
    octoBot.loop.create_task(start_node())

@octoBot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node {node.identifier} is ready!")

async def start_node():
    await octoBot.wait_until_ready()

    await wavelink. NodePool.create_node(
        bot=octoBot, 
        host="127.0.0.1", 
        port="2333", 
        password="youshallnotpass"
    )

octoBot.run(TOKEN)