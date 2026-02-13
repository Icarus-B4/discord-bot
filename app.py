import os
import discord
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_TOKEN")

MAX_RESPONSE_LENGTH = 2000

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

openai_client = OpenAI(
    api_key=PERPLEXITY_API_KEY,
    base_url="https://api.perplexity.ai"
)

chat_history = {}


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    # Eigene Nachrichten ignorieren
    if message.author == client.user:
        return

    # Nur auf Nachrichten reagieren, die mit "!ask" beginnen
    if not message.content.startswith("!ask"):
        return

    question = message.content[5:].strip()
    if not question:
        await message.channel.send("Bitte stelle deine Frage nach `!ask`.")
        return

    user_id = str(message.author.id)

    # Falls noch keine History existiert, Systemnachricht anlegen
    if user_id not in chat_history:
        chat_history[user_id] = [
            {
                "role": "system",
                "content": (
                    "Du bist ein hilfreicher deutschsprachiger Assistent für eine "
                    "Discord‑Trading‑Community. Antworte klar, strukturiert und freundlich."
                ),
            }
        ]

    chat_history[user_id].append({"role": "user", "content": question})

    # Anfrage an Perplexity
    response = openai_client.chat.completions.create(
        model="sonar-medium-online",
        messages=chat_history[user_id],
    )

    assistant_response = response.choices[0].message.content
    chat_history[user_id].append(
        {"role": "assistant", "content": assistant_response}
    )

    # Antwort ggf. in 2000‑Zeichen‑Chunks aufteilen
    for i in range(0, len(assistant_response), MAX_RESPONSE_LENGTH):
        chunk = assistant_response[i : i + MAX_RESPONSE_LENGTH]
        await message.channel.send(chunk)


if __name__ == "__main__":
    client.run(DISCORD_BOT_TOKEN)
