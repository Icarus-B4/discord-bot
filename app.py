import os
import discord
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_TOKEN")
MAX_RESPONSE_LENGTH = 1900  # Etwas kleiner für Free-Tier

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

openai_client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")

chat_history = {}

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message.content.startswith('!ask '):
        return

    question = message.content[5:].strip()
    user_id = str(message.author.id)

    if user_id not in chat_history:
        chat_history[user_id] = [{"role": "system", "content": "Du bist ein hilfreicher Trading-Assistent."}]
    chat_history[user_id].append({"role": "user", "content": question})

    try:
        response = openai_client.chat.completions.create(
            model="sonar-medium-online",
            messages=chat_history[user_id]
        )
        assistant_response = response.choices[0].message.content
        chat_history[user_id].append({"role": "assistant", "content": assistant_response})

        for i in range(0, len(assistant_response), MAX_RESPONSE_LENGTH):
            await message.channel.send(assistant_response[i:i+MAX_RESPONSE_LENGTH])
    except Exception as e:
        await message.channel.send(f"Fehler: {str(e)}")

if __name__ == "__main__":
    client.run(DISCORD_BOT_TOKEN)
