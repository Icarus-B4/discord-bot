import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from openai import OpenAI
import asyncio

# 1. SETUP & EINSTELLUNGEN
load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_TOKEN")
TRADING_HUB_ID =   # Dein Kanal
MAX_RESPONSE_LENGTH = 1900

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Perplexity Client (OpenAI-kompatibel)
openai_client = OpenAI(
    api_key=PERPLEXITY_API_KEY, 
    base_url="https://api.perplexity.ai"
)

# Chat-Gedächtnis
chat_history = {}

# 2. STATUS & INITIALISIERUNG
@bot.event
async def on_ready():
    # Setzt den Text unter dem Bot-Namen
    activity = discord.Activity(
        type=discord.ActivityType.watching, 
        name="over your Trades 📈"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)
    
    print(f'🚀 Trading Bot v4.0 online als {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'✅ {len(synced)} Slash Commands synchronisiert!')
    except Exception as e:
        print(f'❌ Sync Fehler: {e}')

# --- HILFSFUNKTION FÜR PERPLEXITY + QUELLEN + BILDER ---
async def ask_perplexity(user_id, question, system_prompt, use_images=False):
    if user_id not in chat_history:
        chat_history[user_id] = [{"role": "system", "content": system_prompt}]
    
    chat_history[user_id].append({"role": "user", "content": question})

    # return_images: True für KI-generierte Bilder/Web-Charts
    response = openai_client.chat.completions.create(
        model="sonar-pro", 
        messages=chat_history[user_id],
        extra_body={"return_images": use_images}
    )
    
    answer = response.choices[0].message.content
    chat_history[user_id].append({"role": "assistant", "content": answer})
    
    # Bilder und Quellen extrahieren
    image_url = response.images[0] if use_images and hasattr(response, 'images') and response.images else None
    citations = getattr(response, 'citations', [])
    source_text = ""
    if citations:
        source_text = "\n\n**Weiterführende Quellen:**\n" + "\n".join([f"[{i+1}] {url}" for i, url in enumerate(citations)])
    
    return answer, source_text, image_url

# --- COMMAND: /ask (Allgemeine Analyse mit Bildern) ---
@bot.tree.command(name="ask", description="Trading-Analyse mit Bildsuche")
async def ask(interaction: discord.Interaction, frage: str):
    if interaction.channel_id != TRADING_HUB_ID:
        await interaction.response.send_message(f"❌ Nur in <#{TRADING_HUB_ID}> erlaubt!", ephemeral=True)
        return

    await interaction.response.defer()
    try:
        ans, src, img = await ask_perplexity(str(interaction.user.id), frage, "Du bist ein Trading-Experte.", use_images=True)
        embed = discord.Embed(title="Trading Analyse", description=ans, color=discord.Color.blue())
        if src: embed.add_field(name="Referenzen", value=src[:1024], inline=False)
        if img: embed.set_image(url=img)
        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"❌ Fehler: {str(e)}")

# --- COMMAND: /price (Mit Auswahl-Menü) ---
@bot.tree.command(name="price", description="Checke Kurse & Key-Levels")
@app_commands.choices(asset=[
    app_commands.Choice(name="Bitcoin (BTC)", value="BTC"),
    app_commands.Choice(name="Ethereum (ETH)", value="ETH"),
    app_commands.Choice(name="Gold", value="XAUUSD"),
    app_commands.Choice(name="S&P 500", value="SPX"),
    app_commands.Choice(name="Euro/Dollar (EURUSD)", value="EURUSD")
])
async def price(interaction: discord.Interaction, asset: app_commands.Choice[str]):
    if interaction.channel_id != TRADING_HUB_ID:
        await interaction.response.send_message(f"❌ Nur in <#{TRADING_HUB_ID}> erlaubt!", ephemeral=True)
        return

    await interaction.response.defer()
    prompt = f"Aktueller Preis, 24h Trend und wichtige Support/Resistance Level für {asset.name}."
    ans, _, _ = await ask_perplexity(str(interaction.user.id), prompt, "Präziser Markt-Analyst.")
    
    embed = discord.Embed(title=f"Markt-Update: {asset.name}", description=ans, color=discord.Color.green())
    await interaction.followup.send(embed=embed)

# --- COMMAND: /calendar (Wirtschaftsnews) ---
@bot.tree.command(name="calendar", description="Heutige High-Impact Wirtschaftstermine")
async def calendar(interaction: discord.Interaction):
    if interaction.channel_id != TRADING_HUB_ID:
        await interaction.response.send_message(f"❌ Nur in <#{TRADING_HUB_ID}> erlaubt!", ephemeral=True)
        return

    await interaction.response.defer()
    ans, src, _ = await ask_perplexity(str(interaction.user.id), "Wichtige High-Impact Wirtschaftstermine für heute?", "Analyst.")
    await interaction.followup.send(embed=discord.Embed(title="📅 Wirtschaftskalender", description=ans, color=discord.Color.red()))

# --- COMMAND: /pinescript (Coding Hilfe) ---
@bot.tree.command(name="pinescript", description="Hilfe bei TradingView Pine Script")
async def pinescript(interaction: discord.Interaction, frage: str):
    await interaction.response.defer()
    ans, _, _ = await ask_perplexity(str(interaction.user.id), frage, "Du bist ein Pine Script Experte.")
    await interaction.followup.send(embed=discord.Embed(title="💻 Pine Script Helper", description=ans, color=discord.Color.dark_grey()))

# --- COMMAND: /risk (Positionsgröße) ---
@bot.tree.command(name="risk", description="Berechne Risiko & Lot-Size")
async def risk(interaction: discord.Interaction, kapital: float, risiko_prozent: float, stop_loss_pips: float):
    await interaction.response.defer()
    prompt = f"Berechne Positionsgröße für {kapital}€ Konto, {risiko_prozent}% Risiko und {stop_loss_pips} Pips Stop-Loss."
    ans, _, _ = await ask_perplexity(str(interaction.user.id), prompt, "Risk-Management Experte.")
    await interaction.followup.send(embed=discord.Embed(title="⚖️ Risiko-Kalkulator", description=ans, color=discord.Color.orange()))

# --- COMMAND: /clear (Reset) ---
@bot.tree.command(name="clear", description="Chat-Verlauf leeren")
async def clear(interaction: discord.Interaction):
    chat_history.pop(str(interaction.user.id), None)
    await interaction.response.send_message("🧹 Verlauf wurde erfolgreich geleert!")

# 4. BOT STARTEN
bot.run(DISCORD_BOT_TOKEN)
