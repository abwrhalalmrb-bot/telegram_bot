import os
import threading
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 1. إعداد خادم Web مصغر ليعمل مع Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive and Running 24/7!"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# 2. إعداد البوت وتوكن التليجرام
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# دالة القائمة الرئيسية والأزرار الشفافة
def main_menu_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    
    markup.add(InlineKeyboardButton("🛒 شراء رقم افتراضي", callback_data="buy_number"))
    
    markup.add(
        InlineKeyboardButton("💬 عروض WhatsApp", callback_data="whatsapp_offers"),
        InlineKeyboardButton("✈️ عروض Telegram", callback_data="telegram_offers")
    )
    
    markup.add(
        InlineKeyboardButton("🎳 الأكثر توفراً", callback_data="most_available")
    )
    
    markup.add(
        InlineKeyboardButton("🔭 الرشق وشحن الألعاب والبرامج", callback_data="boosting_services")
    )
    
    markup.add(
        InlineKeyboardButton("💎 ربح الأرصدة مجاناً (أكواد وهدايا)", callback_data="free_balance")
    )
    
    markup.add(
        InlineKeyboardButton("📞 الدعم", callback_data="support")
    )
    
    markup.add(
        InlineKeyboardButton("📖 تعليمات وطريقة استخدام البوت", callback_data="instructions")
    )
    
    markup.add(
        InlineKeyboardButton("👤 حسابي", callback_data="my_account")
    )
    
    return markup

# أمر البدء /start
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
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=main_menu_markup(),
        parse_mode="Markdown"
    )

# التعامل مع الضغط على الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    
    if call.data == "buy_number":
        text = (
            "🌐 **قسم شراء الأرقام الوهمية (جميع دول العالم متاحة):**\n\n"
            "اختر التطبيق المطلوب لتفعيل رقم وهمي:\n"
            "• واتساب، تيليجرام، انستقرام، فيسبوك، تيك توك، جميع التطبيقات الأخرى.\n\n"
            "*(الرجاء اختيار الدولة والتطبيق من القائمة الفرعية)*"
        )
    elif call.data == "whatsapp_offers":
        text = "💬 **عروض WhatsApp:**\nأرقام قوية وثابتة لتفعيل تطبيق واتساب وبزنس بضمان كامل."
    elif call.data == "telegram_offers":
        text = "✈️ **عروض Telegram:**\nأرقام مميزة لتفعيل حسابات تيليجرام جاهزة ومضمونة."
    elif call.data == "most_available":
        text = "🎳 **الخدمات الأكثر توفراً وطلباً حالياً:**\nتضم الأرقام الأكثر استقراراً وخدمات الرشق السريعة."
    elif call.data == "boosting_services":
        text = (
            "🔭 **قسم خدمات الرشق الشامل لجميع مواقع التواصل الاجتماعي:**\n\n"
            "• زيادة متابعين (انستقرام، تيك توك، تويتر/X، يوتيوب، سناب شات).\n"
            "• زيادة لايكات، مشاهدات، وتعليقات.\n"
            "• شحن شدات وجواهر الألعاب والبرامج.\n\n"
            "*(جميع خدمات الرشق تتميز بالسرعة والضمان)*"
        )
    elif call.data == "free_balance":
        text = "💎 **ربح الأرصدة مجاناً:**\nتابع قناة البوت يومياً للحصول على أكواد وهدايا رصيد مجانية!"
    elif call.data == "support":
        text = "📞 **الدعم الفني:**\nللتواصل مع الإدارة وحل أي مشكلة تواجهك: @Support_Admin"
    elif call.data == "instructions":
        text = "📖 **تعليمات وطريقة استخدام البوت:**\n1. اختر القسم المناسب.\n2. تأكد من توفر رصيد أو اطلب رصيد مجاني.\n3. تنفيذ الخدمة يتم بشكل فوري وآلي."
    elif call.data == "my_account":
        text = f"👤 **معلومات حسابك:**\n\n• الآيدي: `{user_id}`\n• الرصيد: `0.00$`\n• الطلبات المكتملة: `0`"
    else:
        text = "تم استلام طلبك بنجاح."

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

# تشغيل الخادم والبوت في مسارات مستقلة
if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    print("Bot is running...")
    bot.infinity_polling()
