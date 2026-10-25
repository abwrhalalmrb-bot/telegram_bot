import os
import json
import telebot
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# الآيدي الخاص بك كمشرف (ومعرف حسابك للتواصل)
ADMIN_ID = 6815376911
ADMIN_USERNAME = "akram_matari"  # أو رابط حسابك المباشر
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
    return "Bot is running 24/7!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# القائمة الرئيسية الكاملة
def main_menu_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("🛒 شراء رقم افتراضي", callback_data="buy_number"))
    markup.add(
        InlineKeyboardButton("💬 عروض WhatsApp", callback_data="whatsapp_offers"),
        InlineKeyboardButton("✈️ عروض Telegram", callback_data="telegram_offers")
    )
    markup.add(InlineKeyboardButton("🎳 الأكثر توفراً", callback_data="most_available"))
    markup.add(InlineKeyboardButton("🔭 الرشق وشحن الألعاب والبرامج", callback_data="boosting_services"))
    markup.add(
        InlineKeyboardButton("💳 شحن الرصيد (جيب)", callback_data="deposit"),
        InlineKeyboardButton("👤 حسابي", callback_data="my_account")
    )
    markup.add(InlineKeyboardButton("📞 الدعم الفني", callback_data="support"))
    markup.add(InlineKeyboardButton("📖 تعليمات الاستخدام", callback_data="instructions"))
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
    text = (
        f"مرحباً بك عزيزي {name} في بوت الخدمات الرقمية 🚀\n\n"
        f"👤 الآيدي: `{user_id}`\n"
        f"💰 رصيدك الحالي: `${balance:.2f}`\n\n"
        f"────────────────────\n"
        f"🌟 بوابتك الأولى للأرقام الافتراضية وخدمات الرشق!\n\n"
        f"👇 اختر ما يناسبك من القائمة أدناه:"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu_markup(), parse_mode="Markdown")

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
        
        bot.reply_to(message, f"✅ تم إضافة ${amount} للمستخدم {target_id} بنجاح.")
        try:
            bot.send_message(int(target_id), f"🎉 **تم شحن حسابك بنجاح!**\n\n➕ المبلغ المضاف: `${amount}`\n💰 رصيدك الجديد: `${users[target_id]['balance']:.2f}`", parse_mode="Markdown")
        except:
            pass
    except Exception as e:
        bot.reply_to(message, "⚠️ خطأ في الاستخدام. استخدم:\n`/addbalance ID المبلغ`", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.from_user.id
    bot.answer_callback_query(call.id)
    
    if call.data == "main_menu":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="👇 القائمة الرئيسية للبوت:", reply_markup=main_menu_markup())
        
    elif call.data == "deposit":
        text = (
            f"💳 **قسم شحن الرصيد عبر محفظة (جيب):**\n\n"
            f"لشحن رصيدك، قم بالتحويل إلى المعلومات التالية:\n\n"
            f"📱 **رقم محفظة جيب:** `780089588`\n"
            f"👤 **اسم الحساب:** `اكرم محمد حسن المطري`\n\n"
            f"────────────────────\n"
            f"📩 **خطوة إرسال الإيصال:**\n"
            f"بعد إتمام التحويل، اضغط على الزر أدناه لإرسال صورة الإيصال ورقم الآيدي الخاص بك (`{user_id}`) مباشرة إلى حساب الإدارة للتفعيل الفوري."
        )
        markup = InlineKeyboardMarkup()
        # زر يوجه مباشرة لحسابك الشخصي على تيليجرام
        markup.add(InlineKeyboardButton("📤 إرسال الإيصال والآيدي للإدارة", url=f"tg://user?id={ADMIN_ID}"))
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")
        
    elif call.data == "my_account":
        balance = get_user_balance(user_id)
        text = (
            f"👤 **معلومات حسابك:**\n\n"
            f"• الاسم: {call.from_user.first_name}\n"
            f"• الآيدي: `{user_id}`\n"
            f"• رصيدك المتوفر: `${balance:.2f}`"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💳 شحن الرصيد الآن", callback_data="deposit"))
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")
        
    elif call.data == "buy_number":
        text = "🛒 **قسم شراء الأرقام الافتراضية:**\n\nاختر التطبيق المطلوب لتفعيل رقم وهمي (قيد التجهيز)."
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "whatsapp_offers":
        text = "💬 **عروض WhatsApp:**\n\nأرقام قوية وثابتة لتفعيل واتساب (قيد التجهيز)."
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "telegram_offers":
        text = "✈️ **عروض Telegram:**\n\nأرقام مميزة لتفعيل تيليجرام (قيد التجهيز)."
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "most_available":
        text = "🎳 **الخدمات الأكثر توفراً:**\n\nالأرقام وخدمات الرشق الأكثر طلباً."
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "boosting_services":
        text = "🔭 **قسم خدمات الرشق الشامل:**\n\nاختر المنصة المطلوبة (انستجرام، تيك توك، وغيرها)."
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "support":
        text = "📞 **الدعم الفني:**\n\nللتواصل المباشر مع الإدارة وحل أي مشكلة:"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("👨‍💻 التواصل مع الدعم", url=f"tg://user?id={ADMIN_ID}"))
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "instructions":
        text = "📖 **تعليمات وطريقة الاستخدام:**\n\n1. اشحن رصيدك عبر محفظة جيب.\n2. أرسل الإيصال للإدارة للتفعيل.\n3. اختر الخدمة المطلوبة وتمتع بالسرعة التنفيذية!"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
