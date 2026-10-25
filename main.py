import os
import json
import telebot
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

ADMIN_IDS = [6815376911]
USERS_FILE = 'users.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def get_user_balance(user_id):
    users = load_users()
    return users.get(str(user_id), {}).get('balance', 0.0)

# إعداد سيرفر الويب لـ Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# القائمة الرئيسية
def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("💳 شحن الرصيد (جيب)", callback_data="deposit"),
        InlineKeyboardButton("👤 حسابي", callback_data="my_account")
    )
    markup.add(InlineKeyboardButton("🔭 خدمات الرشق", callback_data="boosting"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    
    users = load_users()
    if str(user_id) not in users:
        users[str(user_id)] = {'balance': 0.0}
        save_users(users)
        
    balance = get_user_balance(user_id)
    text = f"مرحباً {name} 🚀\nرصيدك: ${balance:.2f}\n\nاختر ما يناسبك:"
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

@bot.message_handler(commands=['addbalance'])
def add_balance(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        parts = message.text.split()
        target_id = parts[1]
        amount = float(parts[2])
        
        users = load_users()
        if target_id not in users:
            users[target_id] = {'balance': 0.0}
        users[target_id]['balance'] += amount
        save_users(users)
        
        bot.reply_to(message, f"تم إضافة ${amount} للمستخدم {target_id} بنجاح.")
        bot.send_message(int(target_id), f"🎉 تم شحن حسابك بمبلغ ${amount} بنجاح!")
    except Exception as e:
        bot.reply_to(message, "خطأ في الأمر. استخدم: /addbalance ID المبلغ")

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.from_user.id
    bot.answer_callback_query(call.id) # ضروري جداً لإيقاف علامة التحميل بالزر
    
    if call.data == "deposit":
        text = (
            f"💳 **شحن الرصيد عبر محفظة جيب:**\n\n"
            f"رقم المحفظة: `780089588`\n"
            f"الاسم: `اكرم محمد حسن المطري`\n\n"
            f"بعد التحويل، أرسل الإيصال وآيدي حسابك (`{user_id}`) للدعم."
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")
        
    elif call.data == "my_account":
        balance = get_user_balance(user_id)
        text = f"👤 آيدي: `{user_id}`\n💰 رصيدك: `${balance:.2f}`"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💳 شحن الرصيد", callback_data="deposit"))
        markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")
        
    elif call.data in ["boosting", "back"]:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="القائمة الرئيسية:", reply_markup=main_menu())

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
