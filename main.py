import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# إعدادات البوت الأساسية
TOKEN = "7953256087:AAEIW9d8-G5hJp8rJ2fG9x7W3Z4K2L1M0nQ"
ADMIN_ID = 6815376911
ADMIN_NAME = "اكرم Mohammed Hassan Al-Matari"
JEEB_WALLET = "780089588"

bot = telebot.TeleBot(TOKEN)
user_balances = {}

def get_balance(user_id):
    return user_balances.get(user_id, 0.0)

def update_balance(user_id, amount):
    user_balances[user_id] = get_balance(user_id) + amount

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🛒 خدمات الرشق", callback_data="services"),
        InlineKeyboardButton("💰 محفظتي وشحن الرصيد", callback_data="wallet")
    )
    markup.add(
        InlineKeyboardButton("📞 التواصل والدعم الفني", callback_data="support"),
        InlineKeyboardButton("👤 حسابي", callback_data="account")
    )
    bot.send_message(
        message.chat.id,
        f"مرحباً بك يا غالي في بوت الخدمات الرقمية والرشـق 🚀\n\n"
        f"🔹 الإدارة: {ADMIN_NAME}\n"
        f"🔹 اختر ما يناسبك من القائمة أدناه:",
        reply_markup=markup
    )

@bot.message_handler(commands=['addbalance'])
def add_balance_cmd(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "عذراً، هذا الأمر مخصص للإدارة فقط.")
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(message, "خطأ! استخدم الصيغة الصحيحة:\n`/addbalance user_id amount`", parse_mode="Markdown")
        return
    
    try:
        target_user_id = int(args[1])
        amount = float(args[2])
        update_balance(target_user_id, amount)
        bot.reply_to(message, f"✅ تم بنجاح إضافة `{amount}$` إلى رصيد المستخدم `{target_user_id}`.", parse_mode="Markdown")
        bot.send_message(target_user_id, f"🎉 تم شحن رصيدك بمبلغ `{amount}$` بنجاح بواسطة الإدارة!", parse_mode="Markdown")
    except ValueError:
        bot.reply_to(message, "تأكد من أن الآيدي والمبلغ أرقام صحيحة.")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "wallet":
        user_id = call.from_user.id
        balance = get_balance(user_id)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📤 إرسال إيصال التحويل للإدارة", url=f"https://t.me/A_M_Almatari"))
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        
        text = (
            f"💰 **محفظتك الرقمية:**\n\n"
            f"🔹 رصيدك الحالي: `{balance}$`\n\n"
            f"💳 **لشحن الرصيد عبر محفظة جيب (Jeeb):**\n"
            f"رقم الحساب: `{JEEB_WALLET}`\n"
            f"اسم المستلم: `{ADMIN_NAME}`\n\n"
            f"⚠️ بعد إتمام التحويل، اضغط على زر إرسال الإيصال وأرسل صورة التحويل مع الآيدي الخاص بك للإدارة ليتم شحن رصيدك فوراً."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "support":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("👨‍💻 تواصل مباشر مع المطور/الإدارة", url=f"https://t.me/A_M_Almatari"))
        markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="main_menu"))
        bot.edit_message_text("لأي استفسار أو مشكلة، تواصل معنا مباشرة عبر الزر أدناه:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "account":
        user_id = call.from_user.id
        balance = get_balance(user_id)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="main_menu"))
        bot.edit_message_text(f"👤 **معلومات الحساب:**\n\n🆔 الآيدي: `{user_id}`\n💰 الرصيد: `{balance}$`", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "services":
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("📸 انستجرام", callback_data="cat_insta"),
            InlineKeyboardButton("🎵 تيك توك", callback_data="cat_tiktok")
        )
        markup.add(
            InlineKeyboardButton("✈️ تيليجرام", callback_data="cat_tele"),
            InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")
        )
        bot.edit_message_text("اختر القسم المطلوب:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "main_menu":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🛒 خدمات الرشق", callback_data="services"),
            InlineKeyboardButton("💰 محفظتي وشحن الرصيد", callback_data="wallet")
        )
        markup.add(
            InlineKeyboardButton("📞 التواصل والدعم الفني", callback_data="support"),
            InlineKeyboardButton("👤 حسابي", callback_data="account")
        )
        bot.edit_message_text("مرحباً بك مرة أخرى في القائمة الرئيسية:", call.message.chat.id, call.message.message_id, reply_markup=markup)

if __name__ == '__main__':
    print("Bot is starting...")
    bot.infinity_polling()
