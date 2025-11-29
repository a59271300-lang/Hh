import telebot
import json
from datetime import datetime, timedelta

# === CONFIG ===
TOKEN = "8185627657:AAHWBrtyl3WAoip1ZVHFeS2saVYXWj5L2pk"   # <-- Replace with your BotFather token
ADMIN_ID = 7888759188                # <-- Replace with your Telegram user id (admin)

# === Local JSON database ===
DB_FILE = "users.json"

def load_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Load users
users = load_db()

# Initialize star wallet for existing users
for uid in users:
    if "stars" not in users[uid]:
        users[uid]["stars"] = 0
    if "downloads" not in users[uid]:
        users[uid]["downloads"] = 0
    if "reset_time" not in users[uid]:
        users[uid]["reset_time"] = (datetime.utcnow() + timedelta(hours=24)).timestamp()
    if "premium" not in users[uid]:
        users[uid]["premium"] = False
    if "premium_expiry" not in users[uid]:
        users[uid]["premium_expiry"] = 0
save_db(users)

bot = telebot.TeleBot(TOKEN)

# -------- Helper Functions --------
def get_user(user_id):
    uid = str(user_id)
    if uid not in users:
        users[uid] = {
            "downloads": 0,
            "stars": 0,
            "premium": False,
            "reset_time": (datetime.utcnow() + timedelta(hours=24)).timestamp(),
            "premium_expiry": 0
        }
        save_db(users)
    return users[uid]

def reset_if_needed(user_id):
    user = get_user(user_id)
    now = datetime.utcnow().timestamp()

    # Reset download count every 24 hr
    if now > user["reset_time"]:
        user["downloads"] = 0
        user["reset_time"] = (datetime.utcnow() + timedelta(hours=24)).timestamp()

    # Expire premium if needed
    if user["premium"] and now > user["premium_expiry"]:
        user["premium"] = False
        user["premium_expiry"] = 0

    save_db(users)
    return user

# -------- Commands --------
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "Welcome 🎉\n\n"
        "📌 Free User → 24 hours me 5 videos\n"
        "💎 Premium → Unlimited downloads\n\n"
        "⭐ Subscription Prices ⭐\n"
        "7 Days → 30 Stars\n"
        "15 Days → 50 Stars\n"
        "30 Days → 100 Stars\n\n"
        "➡ Video link bhejo download ke liye.\n\n"
        "💰 Apne Stars check kare: /mystars\n"
        "🎁 Stars add karne ke liye (Admin only): /addstars user_id amount\n"
        "📦 Premium activate karne ke liye: /buypremium days\n"
        "Example: /buypremium 7"
    )

@bot.message_handler(commands=['mystars'])
def mystars(message):
    user = get_user(message.from_user.id)
    bot.reply_to(message, f"🌟 Aapke Stars: {user.get('stars', 0)}")

@bot.message_handler(commands=['addstars'])
def addstars(message):
    if message.from_user.id != ADMIN_ID: 7888759188
        return
    try:
        _, user_id, amount = message.text.split()
        amount = int(amount)
    except:
        bot.reply_to(message, "Use: /addstars user_id amount")
        return

    user = get_user(user_id)
    user['stars'] += amount
    save_db(users)
    bot.reply_to(message, f"User {user_id} ko {amount} Stars add kar diye gaye.")

@bot.message_handler(commands=['premium'])
def premium_cmd(message):
    bot.reply_to(message,
        "🎁 *Premium Subscription Options* 🎁\n\n"
        "⭐ 7 Days = 30 Stars\n"
        "⭐ 15 Days = 50 Stars\n"
        "⭐ 30 Days = 100 Stars\n\n"
        "🎯 Buy premium using: /buypremium days\n"
        "Example: /buypremium 7"
    )

# -------- Purchase premium with stars --------
@bot.message_handler(commands=['buypremium'])
def buy_premium(message):
    user = get_user(message.from_user.id)

    try:
        parts = message.text.split()
        days = int(parts[1])
    except:
        bot.reply_to(message, "Use: /buypremium days (7/15/30)")
        return

    prices = {7: 30, 15: 50, 30: 100}
    if days not in prices:
        bot.reply_to(message, "Valid options: 7 / 15 / 30 days")
        return

    cost = prices[days]
    if user['stars'] < cost:
        bot.reply_to(message, f"❌ Aapke paas enough Stars nahi hain.\n⭐ Required: {cost}\n⭐ Your Stars: {user['stars']}")
        return

    # Deduct stars and activate premium
    user['stars'] -= cost
    user['premium'] = True
    user['premium_expiry'] = (datetime.utcnow() + timedelta(days=days)).timestamp()
    save_db(users)

    bot.reply_to(message, f"🎉 {days} Days Premium activate ho gaya!\n⭐ Stars deducted: {cost}")

# -------- Admin: manual premium activation --------
@bot.message_handler(commands=['setpremium'])
def set_premium(message):
    if message.from_user.id != ADMIN_ID:7888759188
        return

    try:
        args = message.text.split()
        user_id = args[1]
        days = int(args[2])
    except:
        bot.reply_to(message, "Use: /setpremium user_id days")
        return

    user = get_user(user_id)
    user['premium'] = True
    user['premium_expiry'] = (datetime.utcnow() + timedelta(days=days)).timestamp()
    save_db(users)

    bot.reply_to(message, f"User {user_id} ko {days} days ka premium de diya gaya.")

# -------- Main Download Logic (stub) --------
@bot.message_handler(func=lambda m: True)
def download_handler(message):
    # This handler assumes user sends a video link or command to download.
    # Replace the 'process_video_download' stub with your actual downloader logic.
    uid = str(message.from_user.id)
    user = reset_if_needed(uid)

    # Premium → unlimited
    if user["premium"]:
        bot.send_message(message.chat.id, "💎 Premium user → Unlimited downloads! Processing video...")
        # TODO: call your video download & send function here
        return

    # Free user limit = 5 per 24 hours
    if user["downloads"] >= 5:
        time_left = int(user["reset_time"] - datetime.utcnow().timestamp())
        hours = time_left // 3600
        minutes = (time_left % 3600) // 60
        bot.send_message(
            message.chat.id,
            f"❌ Aaj ka limit khatam ho gaya.\n⏳ Try after: {hours}h {minutes}m\n\n💎 Premium lo unlimited ke liye!"
        )
        return

    # Allow download
    users[uid]["downloads"] = users[uid].get("downloads", 0) + 1
    save_db(users)

    bot.send_message(message.chat.id, "✅ Video download request accepted. Processing...")
    # TODO: implement 'process_video_download(message)' to fetch and send the video

# -------- Run --------
if __name__ == "__main__":
    print("Bot is starting...")
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("Bot stopped by user.")