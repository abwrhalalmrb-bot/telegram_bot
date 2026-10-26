import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import os
from flask import Flask
from threading import Thread

# إعدادات البوت والتوكن الخاص بك
TOKEN = "8708102287:AAHavoWuCttSxEhhwQd1TMFN4nX_DdAwSE8"
ADMIN_ID = 6815376911
ADMIN_NAME = "اكرم Mohammed Hassan Al-Matari"
JEEB_WALLET = "780089588"
ADMIN_USERNAME = "A_M_Almatari"

bot = telebot.TeleBot(TOKEN)
user_balances = {}

# سيرفر الويب الوهمي للحفاظ على العلامة الزرقاء في Render
app = Flask('')

@app.route('/')
def home():
    return "Digital Hub Bot is running and active!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def get_balance(user_id):
    return user_balances.get(user_id, 0.0)

def update_balance(user_id, amount):
    user_balances[user_id] = get_balance(user_id) + amount

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    balance = get_balance(user_id)
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🛒 شراء رقم افتراضي", callback_data="buy_number")
    )
    
    row2_1 = InlineKeyboardButton("💬 عروض WhatsApp", callback_data="offers_wa")
    row2_2 = InlineKeyboardButton("✈️ عروض Telegram", callback_data="offers_tg")
    markup.row(row2_1, row2_2)
    
    row3_1 = InlineKeyboardButton("🎲 شحن الرصيد", callback_data="wallet")
    row3_2 = InlineKeyboardButton("🎳 الأكثر توفراً", callback_data="most_used")
    markup.row(row3_1, row3_2)
    
    markup.add(
        InlineKeyboardButton("🚀 الرشق وشحن الألعاب والبرامج", callback_data="services"),
        InlineKeyboardButton("💎 ربح الأرصدة مجاناً (أكواد وهدايا)", callback_data="free_balance")
    )
    
    row6_1 = InlineKeyboardButton("🔄 تحويل الرصيد", callback_data="transfer"),
    row6_2 = InlineKeyboardButton("📞 الدعم", url=f"https://t.me/{ADMIN_USERNAME}")
    markup.row(row6_1[0], row6_2)
    
    markup.add(
        InlineKeyboardButton("📖 تعليمات وطريقة استخدام البوت", callback_data="help"),
        InlineKeyboardButton("👤 حسابي", callback_data="account")
    )
    
    bot.send_message(
        message.chat.id,
        f"👤 **الآيدي:** `{user_id}`\n"
        f"💙 **رصيدك الحالي:** `{balance:.2f} $`\n\n"
        f"━━━━━━━━━━━━━━━\n\n"
        f"🌟 **بوابتك الأولى والأسرع للخدمات الرقمية المتكاملة، الأرقام الافتراضية، والرشـق!**[cite: 10]\n\n"
        f"👇 **اختر ما يناسبك من القائمة أدناه:**",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['addbalance'])
def add_balance_cmd(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "عذراً، هذا الأمر مخصص للإدارة فقط.")
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(message, "⚠️ خطأ! استخدم الصيغة الصحيحة:\n`/addbalance user_id amount`", parse_mode="Markdown")
        return
    
    try:
        target_user_id = int(args[1])
        amount = float(args[2])
        update_balance(target_user_id, amount)
        bot.reply_to(message, f"✅ تم بنجاح إضافة `{amount}$` إلى رصيد المستخدم `{target_user_id}`.", parse_mode="Markdown")
        bot.send_message(target_user_id, f"🎉 تم شحن رصيدك بمبلغ `{amount}$` بنجاح بواسطة الإدارة!", parse_mode="Markdown")
    except ValueError:
        bot.reply_to(message, "⚠️ تأكد من أن الآيدي والمبلغ أرقام صحيحة.")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "wallet":
        user_id = call.from_user.id
        balance = get_balance(user_id)
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📤 إرسال إيصال التحويل للإدارة", url=f"https://t.me/{ADMIN_USERNAME}"),
            InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")
        )
        text = (
            f"💰 **حساب المحفظة الرقمية والشحن:**\n\n"
            f"🔹 رصيدك الحالي: `{balance:.2f}$`\n\n"
            f"💳 **لشحن الرصيد عبر محفظة جيب (Jeeb):**\n"
            f"رقم الحساب: `{JEEB_WALLET}`\n"
            f"اسم المستلم: `{ADMIN_NAME}`\n\n"
            f"⚠️ بعد إتمام التحويل، اضغط على زر إرسال الإيصال وأرسل صورة التحويل مع الآيدي الخاص بك للإدارة ليتم شحن رصيدك فوراً."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "account":
        user_id = call.from_user.id
        balance = get_balance(user_id)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text(f"👤 **معلومات حسابك الشخصي:**\n\n🆔 الآيدي الخاص بك: `{user_id}`\n💰 الرصيد المتاح: `{balance:.2f}$`", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "services":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("📸 انستجرام", callback_data="cat_insta"),
            InlineKeyboardButton("🎵 تيك توك", callback_data="cat_tiktok")
        )
        markup.add(
            InlineKeyboardButton("✈️ تيليجرام", callback_data="cat_tele"),
            InlineKeyboardButton("🎮 شحن الألعاب", callback_data="cat_games")
        )
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text("🚀 **قسـم الرشق وشحن الألعاب والبرامج:**\nاختر القسم المطلوب:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data in ["buy_number", "offers_wa", "offers_tg", "most_used", "free_balance", "transfer", "help", "cat_insta", "cat_tiktok", "cat_tele", "cat_games"]:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📞 التواصل مع الإدارة للطلب", url=f"https://t.me/{ADMIN_USERNAME}"))
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text(
            "📌 **هذا القسم نشط ويتم تنفيذه عبر الإدارة مباشرة:**\n\n"
            "اضغط على زر التواصل أدناه لإرسال طلبك وسيقوم فريقنا بخدمتك فوراً وبأفضل الأسعار!",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup,
            parse_mode="Markdown"
        )

    elif call.data == "main_menu":
        user_id = call.from_user.id
        balance = get_balance(user_id)
        
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("🛒 شراء رقم افتراضي", callback_data="buy_number")
        )
        row2_1 = InlineKeyboardButton("💬 عروض WhatsApp", callback_data="offers_wa")
        row2_2 = InlineKeyboardButton("✈️ عروض Telegram", callback_data="offers_tg")
        markup.row(row2_1, row2_2)
        
        row3_1 = InlineKeyboardButton("🎲 شحن الرصيد", callback_data="wallet")
        row3_2 = InlineKeyboardButton("🎳 الأكثر توفراً", callback_data="most_used")
        markup.row(row3_1, row3_2)
        
        markup.add(
            InlineKeyboardButton("🚀 الرشق وشحن الألعاب والبرامج", callback_data="services"),
            InlineKeyboardButton("💎 ربح الأرصدة مجاناً (أكواد وهدايا)", callback_data="free_balance")
        )
        
        row6_1 = InlineKeyboardButton("🔄 تحويل الرصيد", callback_data="transfer")
        row6_2 = InlineKeyboardButton("📞 الدعم", url=f"https://t.me/{ADMIN_USERNAME}")
        markup.row(row6_1, row6_2)
        
        markup.add(
            InlineKeyboardButton("📖 تعليمات وطريقة استخدام البوت", callback_data="help"),
            InlineKeyboardButton("👤 حسابي", callback_data="account")
        )
        
        bot.edit_message_text(
            f"👤 **الآيدي:** `{user_id}`\n"
            f"💙 **رصيدك الحالي:** `{balance:.2f} $`\n\n"
            f"━━━━━━━━━━━━━━━\n\n"
            f"🌟 **بوابتك الأولى والأسرع للخدمات الرقمية المتكاملة، الأرقام الافتراضية، والرشـق!**[cite: 10]\n\n"
            f"👇 **اختر ما يناسبك من القائمة أدناه:**",
            call.message.chat.id, 
            call.message.message_id, 
            reply_markup=markup,
            parse_mode="Markdown"
        )

if __name__ == '__main__':
    t = Thread(target=run_web)
    t.start()
    
    print("Digital Hub Bot is starting successfully...")
    while True:
        try:
            bot.remove_webhook()
            bot.infinity_polling(skip_pending=True, timeout=90, long_polling_timeout=60)
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(5)
