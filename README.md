# 🤖 AI-Trading Assistant Discord Bot

![Banner](banner.png)

Ein leistungsstarker Discord-Bot, der speziell für **Trading-Communities** entwickelt wurde. Mithilfe der **Perplexity AI API** (Sonar-Modelle) liefert der Bot präzise Antworten, Marktanalysen und Handelsunterstützung direkt in deinen Discord-Server.

---

## ✨ Features

- 🔍 **Echtzeit-Analysen**: Nutzt Perplexity AI für aktuelle Marktdaten und Informationen.
- 💬 **Kontextbewusst**: Speichert den Chat-Verlauf pro Benutzer für flüssige Unterhaltungen.
- 📈 **Trading-Fokus**: Optimiert für Fragen zu Kryptowährungen, Aktien und Marktstrategien.
- ⚡ **Schnelle Interaktion**: Einfache Bedienung über den `!ask` Befehl.
- 🛡️ **Sicher & Robust**: Fehlerbehandlung für lange Nachrichten (automatisches Splitting bei >2000 Zeichen).

---

## 🚀 Erste Schritte

### Voraussetzungen

- **Python 3.8+**
- Ein **Discord Bot Token** (erhältlich im [Discord Developer Portal](https://discord.com/developers/applications))
- Ein **Perplexity AI API Key**

### Installation

1. **Repository klonen** (oder Dateien herunterladen):
   ```bash
   git clone https://github.com/dein-nutzername/discord-bot.git
   cd discord-bot
   ```

2. **Abhängigkeiten installieren**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Konfiguration**:
   Erstelle eine `.env` Datei im Hauptverzeichnis und füge deine Keys hinzu:
   ```env
   DISCORD_TOKEN=dein_discord_bot_token
   PERPLEXITY_API_KEY=dein_perplexity_api_key
   ```

---

## 🛠️ Nutzung

Starte den Bot mit:
```bash
python discord-bot.py
```

### Befehle

| Befehl | Beschreibung | Beispiel |
| :--- | :--- | :--- |
| `!ask [Frage]` | Stellt eine Frage an die KI | `!ask Wie ist der aktuelle Trend bei BTC?` |

Der Bot merkt sich deine vorherigen Fragen, sodass du Rückfragen stellen kannst, wie z.B. *"Und wie sieht es im Vergleich zu ETH aus?"*.

---

## 📦 Tech Stack

- **Sprache**: [Python](https://www.python.org/)
- **Bibliothek**: [discord.py](https://discordpy.readthedocs.io/)
- **KI-Engine**: [Perplexity AI](https://www.perplexity.ai/) (via OpenAI SDK)
- **Environment**: [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Weitere Details findest du in der [LICENSE](https://github.com/Icarus-B4/discord-bot/blob/main/LICENSE) Datei.

---

<p align="center">
  <i>Erstellt mit ❤️ für die Trading-Community.</i>
</p>
