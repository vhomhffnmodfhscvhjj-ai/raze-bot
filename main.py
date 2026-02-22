import telebot
import os
import random
import string
from flask import Flask
from threading import Thread

# --- SERVER FOR RENDER (KEEP ALIVE) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT LOGIC ---
API_TOKEN = '8578580161:AAG4x29Rfdt1m1SZE9eI2obCpi9ygykUR1s'
ADMIN_ID = '8507510168'
DB_FILE = 'dost_list.txt'
TOKEN_FILE = 'tokens.txt'
USED_TOKENS_FILE = 'used_tokens.txt'

bot = telebot.TeleBot(API_TOKEN)
bot.remove_webhook()

def get_data(file_path):
    if not os.path.exists(file_path): return []
    with open(file_path, 'r') as f: return [line.strip() for line in f if line.strip()]

def save_data(file_path, data_list):
    with open(file_path, 'w') as f:
        for item in data_list: f.write(f"{item}\n")

@bot.message_handler(commands=['start'])
def start(message):
    msg = ("👋 𝗛𝗲𝗹𝗹𝗼! 𝗨𝗽𝗱𝗮𝘁𝗲 𝗞𝗲𝗹𝗶𝘆𝗲 @RAZExELITE 𝗦𝗲 𝗧𝗼𝗸𝗲𝗻 𝗟𝗲𝗸𝗮𝗿 𝗠𝘂𝘇𝗲 𝗕𝗵𝗲𝗷𝗶𝘆𝗲\n"
           "👋 हैलो! अपडेट केलीये @RAZExELITE से टोकन लेकर मुझे भेजीये")
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['gen'])
def generate_token(message):
    if str(message.from_user.id) == ADMIN_ID:
        new_token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        tokens = get_data(TOKEN_FILE); tokens.append(new_token); save_data(TOKEN_FILE, tokens)
        bot.reply_to(message, f"🎫 **Naya Token:** `{new_token}`")

@bot.message_handler(commands=['users'])
def list_users(message):
    if str(message.from_user.id) == ADMIN_ID:
        user_ids = get_data(DB_FILE)
        res = "👥 **Users:**\n"
        for uid in user_ids:
            try: res += f"• @{bot.get_chat(uid).username}\n"
            except: res += f"• ID: {uid}\n"
        bot.send_message(ADMIN_ID, res)

@bot.message_handler(func=lambda m: not m.text.startswith('/'))
def handle_token(message):
    user_id, text = str(message.from_user.id), message.text.strip()
    tokens, used = get_data(TOKEN_FILE), get_data(USED_TOKENS_FILE)
    if text in tokens:
        tokens.remove(text); used.append(text); users = get_data(DB_FILE)
        if user_id not in users: users.append(user_id)
        save_data(TOKEN_FILE, tokens); save_data(USED_TOKENS_FILE, used); save_data(DB_FILE, users)
        bot.reply_to(message, "✅ **Token Is Working**")
    elif text in used: bot.reply_to(message, "❌ **Token Already Used**")
    else: bot.reply_to(message, "❌ Galat Token!")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
