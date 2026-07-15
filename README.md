# 🐗 Pumba
 
A multifunctional Telegram bot in Ukrainian, built for everyday use in a friend group / community chat — currency & crypto rates, fuel prices, war-losses tracking, air-raid alerts, weather, mini-games, chat moderation, and more.
 
**Telegram:** [@PumbaBoarBot](https://t.me/PumbaBoarBot)
 
## 📋 About the Project
 
Pumba started as a personal project for a friend group chat and grew into a fairly complete "everyday utility" bot: it pulls live data from several external sources (NBU, CoinGecko, minfin.com.ua, alerts.in.ua, OpenWeather), keeps light chat statistics, runs a couple of games, and gives admins moderation tools — all through simple `/commands` in Ukrainian.
 
## ✨ Features
 
### 💰 Rates & Prices
| Command | Description |
|---|---|
| `/rates` | Currency rates (EUR, USD, PLN, RUB) to UAH, sourced from the NBU |
| `/crypto` | Crypto prices (BTC, ETH, BNB, TON, XRP, ADA, DOGE, SOL) in USD, sourced from CoinGecko |
| `/petrol` | Average fuel prices in Ukraine (A-95 premium, A-95, A-92, diesel, gas) |
 
### 🇺🇦 War-related info
| Command | Description |
|---|---|
| `/alert` | Sends a screenshot of the current air-raid alert map (alerts.in.ua) |
| `/losses` | Russian combat losses since Feb 24, 2022 (personnel, tanks, artillery, aircraft, etc.) |
 
### 🌦️ Weather
| Command | Description |
|---|---|
| `/set_weather` | Choose your city (regional centers of Ukraine) |
| `/weather` | Show current weather for the chosen city |
 
### 🎮 Games
| Command | Description |
|---|---|
| `/tictactoe` | Start a tic-tac-toe game other chat members can join and play |
| `/delete_game` | Clear a stuck tic-tac-toe game (max 1 game per chat) |
| `/rps` | Play rock-paper-scissors against the bot |
| `/number` | Random number (0–100) |
| `/coin` | Coin flip ("Орел" / "Решка") |
| `/random_user` | Pings a random human member of the chat |
 
### 📊 Chat stats & social
| Command | Description |
|---|---|
| `/my_words` | Total number of words you've sent since the bot joined |
| `/top_ten` | Top-10 most active chat members |
| `/birthday` | View/manage the chat's birthday list; the bot congratulates people automatically at 12:00 |
| `/callall` | Mention-everyone flow with an Activate/Cancel confirmation button |
| `/excel` | Export all chat members to an `.xlsx` file |
 
### ℹ️ Other
| Command | Description |
|---|---|
| `/start` | Greeting message |
| `/info` | Full description of all bot functionality |
| Auto-greet/farewell | Welcomes new members and says goodbye when someone leaves |
 
> Full user-facing documentation (in Ukrainian, with data sources for every command) is maintained separately at [telegra.ph](https://telegra.ph/Pumba-07-15-2).
 
## 📡 Data Sources
 
| Data | Source |
|---|---|
| Currency rates (UAH) | [Bank of Ukraine (NBU) public API](https://bank.gov.ua/) |
| Crypto prices | [CoinGecko API](https://www.coingecko.com/en/api) |
| Fuel prices, war losses | [index.minfin.com.ua](https://index.minfin.com.ua/) (losses data originally from the Armed Forces of Ukraine General Staff) |
| Air-raid alert map | [alerts.in.ua](https://alerts.in.ua/) |
| Weather | [OpenWeather](https://openweathermap.org/) |
 
## 🛠️ Tech Stack
 
- **Python 3** + `asyncio`
- **[Telethon](https://docs.telethon.dev/)** — Telegram client/bot framework
- **`schedule`** — cron-like task scheduling (daily birthday checks, etc.)
- **`requests`** + **`BeautifulSoup4`** — fetching & parsing data from currency/fuel/losses sources
- **`playwright`** — headless-browser screenshots (air-raid alert map)
- **`Pillow`** — image conversion (PNG → WebP for Telegram stickers/images)
- **`openpyxl`** (or similar) — generating the `members.xlsx` export
## 📁 Project Structure
 
```
python/
├── main/
│   └── main.py              # Entry point: registers all command handlers
├── config/
│   └── config.py            # Bot client (Telethon) initialization
├── games/
│   ├── tic_tac_toe.py
│   └── rock_paper_scissors.py
├── misc/
│   ├── weather.py            # /weather, /set_weather
│   ├── count_word.py         # /my_words, /top_ten
│   ├── swear.py              # /matuki_on, /matuki_off
│   ├── callback.py           # Inline-button callback handling
│   ├── birthday.py           # /birthday + daily 12:00 check
│   ├── hello_buy.py          # Welcome/goodbye messages
│   ├── all_rates.py          # /rates, /crypto, /petrol
│   ├── other_func.py         # /number, /coin, /alert, /losses, /info, /callall, /random_user, /excel
│   ├── all_word.py           # Global message counter for stats
│   └── admin_func.py         # Admin panel & moderation commands
```
 
## 🚀 Quick Start
 
### Prerequisites
 
- Python 3.x
- A Telegram Bot Token (or Telethon API ID/hash, depending on setup)
- The bot **must be an administrator** of any group chat it's added to, or several features (moderation, member list, welcome messages, etc.) won't work correctly
### Installation and Launch
 
1. **Clone the repository and install dependencies**
```bash
   pip install -r requirements.txt
   playwright install chromium
```
 
2. **Set up environment variables**
```bash
   cp .env.sample .env
```
 
3. **Fill in the `.env` file**
   Open `.env` and provide all required configuration values (Telegram credentials, any third-party API keys such as OpenWeather, etc.).
4. **Run the bot**
```bash
   python python/main/main.py
```
 
## ⚠️ Known Limitations
 
- Some commands only work in group chats (marked in `/info` inside the bot).
- Rate limits on some free public APIs (NBU, CoinGecko, alerts.in.ua) mean commands may occasionally take a moment to respond — if a command fails or only partially completes, wait ~30 seconds and try again.
## 📝 License
 
This project is created for personal use.
 
## 👥 Author
 
Made with ❤️ for friends and community.