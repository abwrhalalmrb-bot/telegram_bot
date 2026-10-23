import os
import telebot
from telebot import types

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_numbers = types.InlineKeyboardButton("📱 أرقام وهمية", callback_data="btn_numbers")
    btn_followers = types.InlineKeyboardButton("🚀 رشق متابعين", callback_data="btn_followers")
    btn_points = types.InlineKeyboardButton("⭐ تجميع نقاط", callback_data="btn_points")
    btn_support = types.InlineKeyboardButton("💬 الدعم الفني", callback_data="btn_support")
    markup.add(btn_numbers, btn_followers)
    markup.add(btn_points, btn_support)
    welcome_text = f"أهلاً بك يا {user_name} في بوت الخدمات المجاني! 👋\n\nاختر الخدمة التي تريدها من الأزرار أدناه:"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    if call.data == "btn_numbers":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📱 **قسم الأرقام الوهمية:**\n\nاختر الدولة التي تريد رقم منها:\n1. 🇺🇸 أمريكا\n2. 🇬🇧 بريطانيا", parse_mode="Markdown")
    elif call.data == "btn_followers":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🚀 **قسم زيادة المتابعين:**\n\nأرسل رابط حسابك وسنبدأ بمعالجة الطلب.", parse_mode="Markdown")
    elif call.data == "btn_points":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "⭐ **تجميع النقاط:**\n\nقم بدعوة أصدقائك لجمع النقاط مجاناً.", parse_mode="Markdown")
    elif call.data == "btn_support":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "💬 للتواصل مع المطور للدعم الفني.")

if __name__ == "__main__":
    print("البوت يعمل الآن...")
    bot.infinity_polling()
