import os
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading

# إعداد خادم الويب لاستيفاء شروط Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active and running 24/7!"

# إعداد التوكن والبوت
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

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

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    welcome_text = (
        f"مرحباً بك عزيزي {first_name} في بوت الخدمات الرقمية 🚀\n\n"
        f"👤 الآيدي: `{user_id}`\n"
        f"💎 رصيدك الحالي: `0.00$`\n\n"
        f"────────────────────\n\n"
        f"🌟 بوابتك الأولى والأسرع للخدمات الرقمية المتكاملة، الأرقام الافتراضية، والرشق!\n\n"
        f"👇 اختر ما يناسبك من القائمة أدناه:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu_markup(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    if call.data == "buy_number":
        text = "🌐 **قسم شراء الأرقام الوهمية (جميع دول العالم متاحة):**\n\nاختر التطبيق المطلوب لتفعيل رقم وهمي."
    elif call.data == "whatsapp_offers":
        text = "💬 **عروض WhatsApp:** أرقام قوية وثابتة لتفعيل واتساب."
    elif call.data == "telegram_offers":
        text = "✈️ **عروض Telegram:** أرقام مميزة لتفعيل تيليجرام."
    elif call.data == "most_available":
        text = "🎳 **الخدمات الأكثر توفراً:** الأرقام وخدمات الرشق الأكثر طلباً."
    elif call.data == "boosting_services":
        text = "🔭 **قسم خدمات الرشق الشامل:** متابعين، لايكات، مشاهدات لكل المنصات."
    elif call.data == "free_balance":
        text = "💎 **ربح الأرصدة مجاناً:** تابع القناة للحصول على أكواد وهدايا."
    elif call.data == "support":
        text = "📞 **الدعم الفني:** للتواصل مع الإدارة: @Support_Admin"
    elif call.data == "instructions":
        text = "📖 **تعليمات الاستخدام:** اختر القسم، تأكد من رصيدك، ويتم التنفيذ فوراً."
    elif call.data == "my_account":
        text = f"👤 **معلومات حسابك:**\n\n• الآيدي: `{user_id}`\n• الرصيد: `0.00$`"
    else:
        text = "تم استلام طلبك بنجاح."

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

# دالة لتشغيل البوت في الخلفية
def run_bot():
    bot.infinity_polling(none_stop=True)

if __name__ == '__main__':
    # تشغيل البوت بخيط مستقل
    t = threading.Thread(target=run_bot)
    t.daemon = True
    t.start()
    
    # تشغيل خادم الويب لفتح البورت المطلوب على Render
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
