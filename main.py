import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import os
import requests
from flask import Flask
from threading import Thread

# إعدادات البوت الأساسية
TOKEN = "8708102287:AAHavoWuCttSxEhhwQd1TMFN4nX_DdAwSE8"
ADMIN_ID = 6815376911
ADMIN_NAME = "اكرم محمد حسن المطري"
JEEB_WALLET = "780089588"
ADMIN_USERNAME = "A_M_Almatari"

# مفتاح الـ API وموقع SMMKings
API_KEY = "2eabc2491e6edcdeeac47c9090e02a96"
API_URL = "https://smmkings.com/api/v2"

# سعر الصرف الثابت: 1 دولار = 800 ريال يمني
EXCHANGE_RATE = 800

bot = telebot.TeleBot(TOKEN)
user_balances = {}

# سيرفر الويب الخفيف لإبقاء البوت نشطاً على Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is active and running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def get_balance(user_id):
    return user_balances.get(user_id, 0.0)

def update_balance(user_id, amount):
    user_balances[user_id] = get_balance(user_id) + amount

def fetch_services():
    try:
        response = requests.post(API_URL, data={'key': API_KEY, 'action': 'services'}, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"API Error: {e}")
    return []

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    balance_yer = get_balance(user_id) * EXCHANGE_RATE
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("🛒 شراء أرقام وهمية وافتراضية", callback_data="numbers"))
    markup.add(
        InlineKeyboardButton("💬 خدمات WhatsApp", callback_data="whatsapp"),
        InlineKeyboardButton("✈️ خدمات Telegram", callback_data="telegram")
    )
    markup.add(
        InlineKeyboardButton("🎲 شحن الرصيد", callback_data="wallet"),
        InlineKeyboardButton("🚀 عرض الخدمات عبر API", callback_data="api_services")
    )
    markup.add(InlineKeyboardButton("📞 التواصل مع الإدارة", url=f"tg://resolve?domain={ADMIN_USERNAME}"))
    markup.add(InlineKeyboardButton("👤 حسابي الشخصي", callback_data="account"))
    
    bot.send_message(
        message.chat.id,
        f"👤 الآيدي: {user_id}\n"
        f"💙 رصيدك: {balance_yer:,.0f} ريال يمني\n\n"
        f"🔥 أهلاً بك في منصتك الاحترافية للخدمات الرقمية والرشق بالريال اليمني!\n"
        f"اختر ما يناسبك من القائمة أدناه:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "wallet":
        user_id = call.from_user.id
        balance_yer = get_balance(user_id) * EXCHANGE_RATE
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📤 إرسال إيصال التحويل للإدارة", url=f"tg://resolve?domain={ADMIN_USERNAME}"))
        markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="main_menu"))
        bot.edit_message_text(
            f"💰 محفظة الشحن:\n\n"
            f"رصيدك الحالي: {balance_yer:,.0f} ريال يمني\n"
            f"لشحن الرصيد عبر محفظة جيب (Jeeb):\n"
            f"رقم الحساب: {JEEB_WALLET}\n"
            f"اسم المستلم: {ADMIN_NAME}\n"
            f"سعر الصرف: 1 دولار = {EXCHANGE_RATE} ريال",
            call.message.chat.id, call.message.message_id, reply_markup=markup
        )

    elif call.data == "account":
        user_id = call.from_user.id
        balance_yer = get_balance(user_id) * EXCHANGE_RATE
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="main_menu"))
        bot.edit_message_text(
            f"👤 معلومات الحساب:\n\nالآيدي: {user_id}\nالرصيد: {balance_yer:,.0f} ريال يمني",
            call.message.chat.id, call.message.message_id, reply_markup=markup
        )

    elif call.data == "api_services":
        bot.edit_message_text("🔄 جاري الاتصال بموقع SMMKings...", call.message.chat.id, call.message.message_id)
        services = fetch_services()
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📞 طلب خدمة محددة عبر الإدارة", url=f"tg://resolve?domain={ADMIN_USERNAME}"))
        markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="main_menu"))
        
        if services and isinstance(services, list):
            text = "🚀 عينة من الخدمات المتاحة حالياً:\n\n"
            for s in services[:10]:
                name = s.get('name', 'خدمة')
                rate_usd = float(s.get('rate', 0))
                rate_yer = rate_usd * EXCHANGE_RATE
                text += f"🔹 {name}\n💰 السعر لكل 1000: {rate_yer:,.0f} ريال\n\n"
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            bot.edit_message_text("⚠️ تعذر جلب الخدمات مؤقتاً، تواصل مع الإدارة للطلب المباشر.", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data in ["numbers", "whatsapp", "telegram"]:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📞 التواصل مع الإدارة لتنفيذ الطلب فوراً", url=f"tg://resolve?domain={ADMIN_USERNAME}"))
        markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="main_menu"))
        bot.edit_message_text(
            "🌟 لطلب هذه الخدمة بدقة وسرعة، يرجى التواصل مباشرة مع الإدارة لتحديد التفاصيل وإتمام الطلب.",
            call.message.chat.id, call.message.message_id, reply_markup=markup
        )

    elif call.data == "main_menu":
        user_id = call.from_user.id
        balance_yer = get_balance(user_id) * EXCHANGE_RATE
        
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("🛒 شراء أرقام وهمية وافتراضية", callback_data="numbers"))
        markup.add(
            InlineKeyboardButton("💬 خدمات WhatsApp", callback_data="whatsapp"),
            InlineKeyboardButton("✈️ خدمات Telegram", callback_data="telegram")
        )
        markup.add(
            InlineKeyboardButton("🎲 شحن الرصيد", callback_data="wallet"),
            InlineKeyboardButton("🚀 عرض الخدمات عبر API", callback_data="api_services")
        )
        markup.add(InlineKeyboardButton("📞 التواصل مع الإدارة", url=f"tg://resolve?domain={ADMIN_USERNAME}"))
        markup.add(InlineKeyboardButton("👤 حسابي الشخصي", callback_data="account"))
        
        bot.edit_message_text(
            f"👤 الآيدي: {user_id}\n"
            f"💙 رصيدك: {balance_yer:,.0f} ريال يمني\n\n"
            f"🔥 أهلاً بك في منصتك الاحترافية للخدمات الرقمية والرشق بالريال اليمني!\n"
            f"اختر ما يناسبك من القائمة أدناه:",
            call.message.chat.id, call.message.message_id, reply_markup=markup
        )

if __name__ == '__main__':
    t = Thread(target=run_web)
    t.start()
    
    print("Bot is starting...")
    while True:
        try:
            bot.remove_webhook()
            bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=30)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)
