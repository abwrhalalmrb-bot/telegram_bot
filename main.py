import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

# إعدادات البوت والتوكن الخاص بك
TOKEN = "8708102287:AAHavoWuCttSxEhhwQd1TMFN4nX_DdAwSE8"
ADMIN_ID = 6815376911
ADMIN_NAME = "اكرم Mohammed Hassan Al-Matari"
JEEB_WALLET = "780089588"
ADMIN_USERNAME = "A_M_Almatari"

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
        InlineKeyboardButton("🛒 قسـم خدمات الرشق", callback_data="services"),
        InlineKeyboardButton("💰 محفظتي وشحن الرصيد", callback_data="wallet")
    )
    markup.add(
        InlineKeyboardButton("📞 التواصل والدعم الفني", url=f"https://t.me/{ADMIN_USERNAME}"),
        InlineKeyboardButton("👤 حسابي الشخصي", callback_data="account")
    )
    bot.send_message(
        message.chat.id,
        f"🌟 **أهلاً بك يا غالي في بوت الخدمات الرقمية والرشـق** 🚀\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🔹 **الإدارة:** {ADMIN_NAME}\n"
        f"🔹 **حالة البوت:** شغال ومنتظم 🟢\n"
        f"━━━━━━━━━━━━━━━\n"
        f"اختر ما يناسبك من القائمة الاحترافية أدناه للبدء:",
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
            f"🔹 رصيدك الحالي: `{balance}$`\n\n"
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
        bot.edit_message_text(f"👤 **معلومات حسابك الشخصي:**\n\n🆔 الآيدي الخاص بك: `{user_id}`\n💰 الرصيد المتاح: `{balance}$`", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "services":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("📸 انستجرام", callback_data="cat_insta"),
            InlineKeyboardButton("🎵 تيك توك", callback_data="cat_tiktok")
        )
        markup.add(
            InlineKeyboardButton("✈️ تيليجرام", callback_data="cat_tele"),
            InlineKeyboardButton("📘 فيسبوك", callback_data="cat_fb")
        )
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text("🛒 **اختر المنصة المطلوبة لخدمات الرشق الاحترافية:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "cat_insta":
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("👥 رشق متابعين انستجرام (ضمان)", callback_data="ord_insta_followers"),
            InlineKeyboardButton("❤️ رشق لايكات انستجرام", callback_data="ord_insta_likes"),
            InlineKeyboardButton("👁️ مشاهدات ريلز انستجرام", callback_data="ord_insta_views"),
            InlineKeyboardButton("🔙 رجوع للأقسام", callback_data="services")
        )
        bot.edit_message_text("📸 **خدمات انستجرام المتاحة:**\nاختر الخدمة المطلوبة:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "cat_tiktok":
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("👥 رشق متابعين تيك توك", callback_data="ord_tt_followers"),
            InlineKeyboardButton("❤️ رشق لايكات تيك توك", callback_data="ord_tt_likes"),
            InlineKeyboardButton("👁️ مشاهدات فيديو تيك توك", callback_data="ord_tt_views"),
            InlineKeyboardButton("🔙 رجوع للأقسام", callback_data="services")
        )
        bot.edit_message_text("🎵 **خدمات تيك توك المتاحة:**\nاختر الخدمة المطلوبة:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "cat_tele":
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("👥 رشق أعضاء قناة تيليجرام", callback_data="ord_tele_members"),
            InlineKeyboardButton("👁️ مشاهدات منشورات تيليجرام", callback_data="ord_tele_views"),
            InlineKeyboardButton("🔙 رجوع للأقسام", callback_data="services")
        )
        bot.edit_message_text("✈️ **خدمات تيليجرام المتاحة:**\nاختر الخدمة المطلوبة:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "cat_fb":
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("👥 رشق متابعين صفحة فيسبوك", callback_data="ord_fb_followers"),
            InlineKeyboardButton("🔙 رجوع للأقسام", callback_data="services")
        )
        bot.edit_message_text("📘 **خدمات فيسبوك المتاحة:**\nاختر الخدمة المطلوبة:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("ord_"):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🛒 اطلب الآن عبر التواصل مع الإدارة", url=f"https://t.me/{ADMIN_USERNAME}"))
        markup.add(InlineKeyboardButton("🔙 رجوع للأقسام", callback_data="services"))
        bot.edit_message_text(
            "📌 **لتأكيد طلب هذه الخدمة:**\n\n"
            "يرجى التواصل مباشرة مع الإدارة عبر الزر أدناه وإرسال:\n"
            "1. رابط الحساب أو المنشور\n"
            "2. الكمية المطلوبة\n"
            "ليتم تنفيذ طلبك فوراً وبشكل يدوي آمن!",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup,
            parse_mode="Markdown"
        )

    elif call.data == "main_menu":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🛒 قسـم خدمات الرشق", callback_data="services"),
            InlineKeyboardButton("💰 محفظتي وشحن الرصيد", callback_data="wallet")
        )
        markup.add(
            InlineKeyboardButton("📞 التواصل والدعم الفني", url=f"https://t.me/{ADMIN_USERNAME}"),
            InlineKeyboardButton("👤 حسابي الشخصي", callback_data="account")
        )
        bot.edit_message_text(
            f"🌟 **القائمة الرئيسية:**\n\n"
            f"🔹 الإدارة: {ADMIN_NAME}\n"
            f"🔹 اختر ما يناسبك من الخيارات أدناه:",
            call.message.chat.id, 
            call.message.message_id, 
            reply_markup=markup,
            parse_mode="Markdown"
        )

if __name__ == '__main__':
    print("Bot is starting professionally...")
    while True:
        try:
            bot.remove_webhook()
            bot.infinity_polling(skip_pending=True, timeout=90, long_polling_timeout=60)
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(5)
