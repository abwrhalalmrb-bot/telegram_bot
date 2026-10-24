import os
import json
import telebot
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# التوكن الخاص بالبوت
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# الآيدي الخاص بك كمشرف للبوت
ADMIN_IDS = [6815376911]

# ملف حفظ أرصدة المستخدمين
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
    str_id = str(user_id)
    return users.get(str_id, {}).get('balance', 0.0)

def set_user_balance(user_id, amount):
    users = load_users()
    str_id = str(user_id)
    if str_id not in users:
        users[str_id] = {'balance': 0.0}
    users[str_id]['balance'] = round(amount, 2)
    save_users(users)

def add_user_balance(user_id, amount):
    current = get_user_balance(user_id)
    set_user_balance(user_id, current + amount)

# إعداد سيرفر ويب وهمي لمنع الـ TimeOut على Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is active and running 24/7!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# القائمة الرئيسية
def main_menu_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("🛒 شراء رقم افتراضي", callback_data="buy_number"))
    markup.add(
        InlineKeyboardButton("💬 عروض WhatsApp", callback_data="whatsapp_offers"),
        InlineKeyboardButton("✈️ عروض Telegram", callback_data="telegram_offers")
    )
    markup.add(InlineKeyboardButton("🔭 الرشق وشحن الألعاب والبرامج", callback_data="boosting_services"))
    markup.add(
        InlineKeyboardButton("💳 شحن الرصيد (جيب)", callback_data="deposit"),
        InlineKeyboardButton("👤 حسابي", callback_data="my_account")
    )
    markup.add(InlineKeyboardButton("📞 الدعم الفني", callback_data="support"))
    markup.add(InlineKeyboardButton("📖 تعليمات الاستخدام", callback_data="instructions"))
    return markup

# أمر البدء /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    
    # التأكد من تسجيل المستخدم في القاعدة
    users = load_users()
    if str(user_id) not in users:
        users[str(user_id)] = {'balance': 0.0, 'name': first_name}
        save_users(users)
        
    balance = get_user_balance(user_id)
    
    welcome_text = (
        f"مرحباً بك عزيزي {first_name} في بوت الخدمات الرقمية 🚀\n\n"
        f"👤 الآيدي: `{user_id}`\n"
        f"💰 رصيدك الحالي: `${balance:.2f}`\n\n"
        f"────────────────────\n"
        f"🌟 بوابتك الأولى للأرقام الافتراضية وخدمات الرشق!\n\n"
        f"👇 اختر ما يناسبك من القائمة أدناه:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu_markup(), parse_mode="Markdown")

# أوامر الإدارة لتزويد الرصيد
@bot.message_handler(commands=['addbalance'])
def handle_add_balance(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        amount = float(parts[2])
        
        add_user_balance(target_id, amount)
        new_balance = get_user_balance(target_id)
        
        bot.reply_to(message, f"✅ تم إشعار وتزويد الحساب برصيد!\n\n🆔 المستخدم: `{target_id}`\n➕ المبلغ المضاف: `${amount}`\n💰 الرصيد الجديد: `${new_balance:.2f}`", parse_mode="Markdown")
        
        # إشعار المستخدم تلقائياً
        try:
            bot.send_message(target_id, f"🎉 **تم شحن حسابك بنجاح!**\n\n➕ المبلغ المضاف: `${amount}`\n💰 رصيدك الحالي: `${new_balance:.2f}`", parse_mode="Markdown")
        except:
            pass
    except Exception as e:
        bot.reply_to(message, "⚠️ **طريقة الاستخدام الخاطئة!**\n\nاستخدم الأمر بالشكل التالي:\n`/addbalance USER_ID AMOUNT`\nمثال:\n`/addbalance 6815376911 5.0`", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    balance = get_user_balance(user_id)
    
    if call.data == "main_menu":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="👇 القائمة الرئيسية للبوت، اختر ما يناسبك:",
            reply_markup=main_menu_markup()
        )
    elif call.data == "deposit":
        text = (
            f"💳 **قسم شحن الرصيد عبر محفظة (جيب):**\n\n"
            f"لشحن رصيدك داخل البوت، يرجى تحويل المبلغ المطلوب إلى حسابنا في محفظة جيب التالية:\n\n"
            f"📱 **رقم محفظة جيب:** `780089588`\n"
            f"👤 **اسم الحساب:** `اكرم محمد حسن المطري`\n\n"
            f"────────────────────\n"
            f"📩 **بعد التحويل:**\n"
            f"يرجى إرسال صورة إيصال التحويل ورقم الآيدي الخاص بك (`{user_id}`) إلى الدعم الفني ليتم تفعيل الرصيد فوراً.\n\n"
            f"👨‍💻 **تواصل مع الدعم:** @Support_Admin"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")
        
    elif call.data == "my_account":
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
        
    elif call.data == "boosting_services":
        text = "🔭 **قسم خدمات الرشق الشامل:**\n\nاختر المنصة المطلوبة (قريباً سيتم ربط خدمات الرشق التفصيلية)."
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")

    elif call.data in ["buy_number", "whatsapp_offers", "telegram_offers", "support", "instructions"]:
        text = f"تم اختيار: {call.data}. قسم قيد التجهيز وربط الأرصدة."
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
