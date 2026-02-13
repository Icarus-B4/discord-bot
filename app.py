import os
from dotenv import load_dotenv
import discord

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Bot online: {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '!test':
        await message.channel.send('✅ Discord funktioniert!')

client.run(DISCORD_TOKEN)
