# Telegram Video Downloader Bot (Local JSON Edition)

This package contains a ready-to-run Telegram bot (Python) that:
- Uses a local `users.json` file as a lightweight database.
- Implements a **star wallet**, admin commands to add stars.
- Allows users to **purchase premium** using stars (7/15/30 days packages).
- Free users can download up to **5 videos per 24 hours**. Premium users have unlimited downloads.
- Includes placeholders where you should add your video-download logic.

## Files in this package
- `bot.py` - Main bot script (edit TOKEN and ADMIN_ID).
- `users.json` - Local JSON database (will be updated automatically).
- `README.md` - This file.

## Setup
1. Install Python (3.8+ recommended).
2. Install required package:
   ```
   pip install pyTelegramBotAPI
   ```
3. Edit `bot.py`:
   - Replace `TOKEN = "8185627657:AAHWBrtyl3WAoip1ZVHFeS2saVYXWj5L2pk"` with the token you get from BotFather.
   - Replace `ADMIN_ID = 7888759188` with your Telegram user id (so admin commands work).
4. Run:
   ```
   python bot.py
   ```

## Admin Commands
- `/addstars user_id amount` — Add stars to a user (admin-only).
- `/setpremium user_id days` — Manually activate premium for a user (admin-only).

## User Commands
- `/start` — Info and usage.
- `/mystars` — Check your stars.
- `/premium` — Show premium packages.
- `/buypremium days` — Buy premium for 7/15/30 days using stars.

## Integrating downloader
In `bot.py`, replace the stub inside `download_handler` with your actual video downloader logic
(e.g., using `yt-dlp`, `pytube`, or site-specific APIs). Be mindful of copyright and platform terms.

## Notes
- This local JSON approach is simple for testing and small bots. For production, use a proper DB (MongoDB, PostgreSQL).
- Keep your token secret.

Happy coding! 🚀
