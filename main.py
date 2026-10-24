import os
import telebot
import requests
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# إعدادات موقع PRM4u API
PRM_API_URL = "https://prm4u.com/api/v2"
PRM_API_KEY = "d01321b883441d3a14d34b7170237551"

# دالة لجلب رصيد الحساب من PRM4u
def get_prm_balance():
    try:
        data = {
            'key': PRM_API_KEY,
            'action': 'balance'
        }
        response = requests.post(PRM_API_URL, data=data).json()
        if 'balance' in response:
            return f"{response['balance']} {response.get('currency', '$')}"
        return "0.00$"
    except:
        return "0.00$"

# دالة لجلب قائمة الخدمات من PRM4u
def get_prm_services():
    try:
        data = {
            'key': PRM_API_KEY,
            'action': 'services'
        }
        response = requests.post(PRM_API_URL, data=data).json()
        return response if isinstance(response, list) else []
    except:
        return []

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
    markup.add(InlineKeyboardButton("🎳 الأكثر توفراً", callback_data="most_available"))
    markup.add(InlineKeyboardButton("🔭 الرشق وشحن الألعاب والبرامج", callback_data="boosting_services"))
    markup.add(InlineKeyboardButton("💎 ربح الأرصدة مجاناً (أكواد وهدايا)", callback_data="free_balance"))
    markup.add(InlineKeyboardButton("📞 الدعم", callback_data="support"))
    markup.add(InlineKeyboardButton("📖 تعليمات وطريقة استخدام البوت", callback_data="instructions"))
    markup.add(InlineKeyboardButton("👤 حسابي", callback_data="my_account"))
    return markup

# قائمة منصات الرشق
def boosting_platforms_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📸 Instagram", callback_data="plat_Instagram"),
        InlineKeyboardButton("🎵 TikTok", callback_data="plat_TikTok")
    )
    markup.add(
        InlineKeyboardButton("✈️ Telegram", callback_data="plat_Telegram"),
        InlineKeyboardButton("▶️ YouTube", callback_data="plat_YouTube")
    )
    markup.add(
        InlineKeyboardButton("📘 Facebook", callback_data="plat_Facebook"),
        InlineKeyboardButton("🐦 Twitter", callback_data="plat_Twitter")
    )
    markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    balance = get_prm_balance()
    
    welcome_text = (
        f"مرحباً بك عزيزي {first_name} في بوت الخدمات الرقمية 🚀\n\n"
        f"👤 الآيدي: `{user_id}`\n"
        f"💎 رصيد المنصة: `{balance}`\n\n"
        f"────────────────────\n\n"
        f"🌟 بوابتك الأولى والأسرع للخدمات الرقمية المتكاملة، الأرقام الافتراضية، والرشق!\n\n"
        f"👇 اختر ما يناسبك من القائمة أدناه:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu_markup(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    
    if call.data == "main_menu":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="👇 القائمة الرئيسية للبوت، اختر ما يناسبك:",
            reply_markup=main_menu_markup()
        )
    elif call.data == "buy_number":
        text = "🌐 **قسم شراء الأرقام الوهمية:**\n\nاختر التطبيق المطلوب لتفعيل رقم وهمي."
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    elif call.data == "whatsapp_offers":
        text = "💬 **عروض WhatsApp:** أرقام قوية وثابتة لتفعيل واتساب."
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    elif call.data == "telegram_offers":
        text = "✈️ **عروض Telegram:** أرقام مميزة لتفعيل تيليجرام."
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    elif call.data == "most_available":
        text = "🎳 **الخدمات الأكثر توفراً:** الأرقام وخدمات الرشق الأكثر طلباً."
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    elif call.data == "boosting_services":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🔭 **قسم خدمات الرشق الشامل:**\nاختر المنصة المطلوبة لعرض خدماتها:",
            reply_markup=boosting_platforms_markup()
        )
    elif call.data.startswith("plat_"):
        platform_name = call.data.replace("plat_", "")
        services = get_prm_services()
        
        # تصفية الخدمات التي تنتمي للمنصة المختارة
        filtered_services = [s for s in services if platform_name.lower() in s.get('category', '').lower() or platform_name.lower() in s.get('name', '').lower()]
        
        if not filtered_services:
            # إذا لم يتم العثور على مطابقة دقيقة بالاسم، نعرض عينة من الخدمات أو رسالة
            text = f"📱 **خدمات {platform_name}:**\n\nعفواً، لم يتم العثور على خدمات مباشرة لهذا القسم حالياً أو جارٍ تحديثها."
        else:
            text = f"📱 **قائمة خدمات {platform_name} المتاحة:**\n\n"
            for s in filtered_services[:10]:  # نعرض أول 10 خدمات كمثال حتى لا تكون الرسالة طويلة جداً
                text += f"🔹 **{s.get('name')}**\n🆔 رقم الخدمة: `{s.get('service')}`\n💰 السعر لكل 1000: `${s.get('rate')}`\n\n"
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع لأقسام الرشق", callback_data="boosting_services"))
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=markup,
            parse_mode="Markdown"
        )
    elif call.data == "free_balance":
        text = "💎 **ربح الأرصدة مجاناً:** تابع القناة للحصول على أكواد وهدايا."
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    elif call.data == "support":
        text = "📞 **الدعم الفني:** للتواصل مع الإدارة: @Support_Admin"
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    elif call.data == "instructions":
        text = "📖 **تعليمات الاستخدام:** اختر القسم، تأكد من رصيدك، ويتم التنفيذ فوراً."
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    elif call.data == "my_account":
        balance = get_prm_balance()
        text = f"👤 **معلومات حسابك:**\n\n• الآيدي: `{user_id}`\n• رصيد المنصة: `{balance}`"
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
