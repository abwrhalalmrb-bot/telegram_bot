import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import os
import requests
from flask import Flask
from threading import Thread

# إعدادات البوت والتوكن الخاص بك
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
    return "SMM Pro Bot is running and active!"

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
def send_welcome(message):
    user_id = message.from_user.id
    balance_yer = get_balance(user_id) * EXCHANGE_RATE
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🛒 شراء أرقام وهمية وافتراضية مضمونة", callback_data="buy_number")
    )
    
    row2_1 = InlineKeyboardButton("💬 عروض WhatsApp", callback_data="offers_wa")
    row2_2 = InlineKeyboardButton("✈️ عروض Telegram", callback_data="offers_tg")
    markup.row(row2_1, row2_2)
    
    row3_1 = InlineKeyboardButton("🎲 شحن الرصيد", callback_data="wallet")
    row3_2 = InlineKeyboardButton("🎳 الأكثر طلباً وتوفراً", callback_data="most_used")
    markup.row(row3_1, row3_2)
    
    markup.add(
        InlineKeyboardButton("🚀 رشق جميع منصات التواصل الاجتماعي (SMM)", callback_data="services")
    )
    
    row5_1 = InlineKeyboardButton("📞 التواصل مع الإدارة", url=f"tg://resolve?domain={ADMIN_USERNAME}")
    row5_2 = InlineKeyboardButton("🛠️ الدعم الفني", url=f"tg://resolve?domain={ADMIN_USERNAME}")
    markup.row(row5_1, row5_2)
    
    markup.add(
        InlineKeyboardButton("📖 تعليمات وطريقة استخدام البوت", callback_data="help"),
        InlineKeyboardButton("👤 حسابي الشخصي", callback_data="account")
    )
    
    bot.send_message(
        message.chat.id,
        f"👤 الآيدي: {user_id}\n"
        f"💙 رصيدك الحالي: {balance_yer:,.0f} ريال يمني\n\n"
        f"━━━━━━━━━━━━━━━\n\n"
        f"🔥 أهلاً بك في منصتك الاحترافية الأولى والأسرع!\n\n"
        f"💎 نبذة عنا:\n"
        f"نحن بوابتك الموثوقة لخدمات الرشق المتكاملة لجميع وسائل التواصل الاجتماعي، وتوفير الأرقام الوهمية والافتراضية بأعلى جودة وضمانة حصرية.\n"
        f"🛡️ موثق ومعتمد من شركة SMM العالمية لضمان السرعة والأمان!\n\n"
        f"👇 اختر ما يناسبك من القائمة أدناه:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "wallet":
        user_id = call.from_user.id
        balance_yer = get_balance(user_id) * EXCHANGE_RATE
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📤 إرسال إيصال التحويل للإدارة", url=f"tg://resolve?domain={ADMIN_USERNAME}"),
            InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")
        )
        text = (
            f"💰 حساب المحفظة الرقمية والشحن:\n\n"
            f"🔹 رصيدك الحالي: {balance_yer:,.0f} ريال يمني\n\n"
            f"💳 لشحن الرصيد عبر محفظة جيب (Jeeb):\n"
            f"رقم الحساب: {JEEB_WALLET}\n"
            f"اسم المستلم: {ADMIN_NAME}\n"
            f"💱 سعر الصرف المعتمد: 1 دولار = {EXCHANGE_RATE} ريال\n\n"
            f"⚠️ بعد إتمام التحويل، اضغط على زر إرسال الإيصال وتواصل معنا لإرسال صورة التحويل ليتم شحن رصيدك فوراً."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "account":
        user_id = call.from_user.id
        balance_yer = get_balance(user_id) * EXCHANGE_RATE
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text(f"👤 معلومات حسابك الشخصي:\n\n🆔 الآيدي الخاص بك: {user_id}\n💰 الرصيد المتاح: {balance_yer:,.0f} ريال يمني\n👨‍💼 المسؤول: {ADMIN_NAME}", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "services":
        # القائمة الخاصة بأقسام المنصات المنفصلة
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("💬 قسم WhatsApp", callback_data="cat_whatsapp"),
            InlineKeyboardButton("📘 قسم Facebook", callback_data="cat_facebook")
        )
        markup.add(
            InlineKeyboardButton("📸 قسم Instagram", callback_data="cat_instagram"),
            InlineKeyboardButton("🎵 قسم TikTok", callback_data="cat_tiktok")
        )
        markup.add(
            InlineKeyboardButton("✈️ قسم Telegram", callback_data="cat_telegram"),
            InlineKeyboardButton("🌐 باقي الخدمات العامة", callback_data="cat_all")
        )
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text("🚀 **اختر المنصة المطلوبة لعرض الخدمات المتاحة بالأسعار اليمنية:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("cat_"):
        platform_key = call.data.split("_")[1]
        bot.edit_message_text("🔄 جاري جلب الخدمات وتحديث الأسعار بالريال اليمني...", call.message.chat.id, call.message.message_id)
        
        services = fetch_services()
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📞 طلب الخدمة عبر الإدارة فوراً", url=f"tg://resolve?domain={ADMIN_USERNAME}"))
        markup.add(InlineKeyboardButton("🔙 رجوع لأقسام المنصات", callback_data="services"))
        
        if services and isinstance(services, list):
            text = "📋 **قائمة الخدمات المتوفرة (معتمدة بالريال اليمني):**\n\n"
            count = 0
            for s in services:
                name = s.get('name', '').lower()
                orig_name = s.get('name', 'خدمة رقمية')
                rate_usd = float(s.get('rate', 0))
                rate_yer = rate_usd * EXCHANGE_RATE
                
                # فلترة الخدمات حسب المنصة التي اختارها المستخدم
                matched = False
                if platform_key == "whatsapp" and ("whatsapp" in name or "واتساب" in name):
                    matched = True
                elif platform_key == "facebook" and ("facebook" in name or "فيسبوك" in name):
                    matched = True
                elif platform_key == "instagram" and ("instagram" in name or "انستجرام" in name or "انستغرام" in name):
                    matched = True
                elif platform_key == "tiktok" and ("tiktok" in name or "تيك توك" in name):
                    matched = True
                elif platform_key == "telegram" and ("telegram" in name or "تيليجرام" in name or "تلجرام" in name):
                    matched = True
                elif platform_key == "all":
                    matched = True
                
                if matched and count < 10:  # عرض حتى 10 خدمات لكل قسم لتجنب طول الرسالة
                    text += f"🔹 **اسم المنتج:** {orig_name}\n"
                    text += f"💰 **سعر المنتج (لكل 1000):** `{rate_yer:,.0f} ريال يمني`\n"
                    text += f"🛡️ **الضمان:** ضمان سنة / جودة عالية وسريعة\n"
                    text += f"━━━━━━━━━━━━━━━\n\n"
                    count += 1
            
            if count == 0:
                text = "⚠️ عذراً، لا توجد خدمات مطابقة حالياً لهذا القسم، يمكنك طلبها مباشرة عبر الإدارة."
            
            try:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            except Exception:
                bot.edit_message_text("✅ تم تحميل الخدمات بنجاح.\n\nلطلب الخدمة فوراً بالاسم والرابط، تواصل مع الإدارة:", call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            bot.edit_message_text("⚠️ تعذر جلب الخدمات من الموقع حالياً، تواصل مع الإدارة مباشرة.", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data in ["buy_number", "offers_wa", "offers_tg", "most_used", "help"]:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📞 التواصل مع الإدارة لتنفيذ الطلب فوراً", url=f"tg://resolve?domain={ADMIN_USERNAME}"))
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        
        msg_text = (
            f"🌟 قسم الخدمات المميزة والمضمونة (SMM):\n\n"
            f"• الأسعار محسوبة بناءً على سعر الصرف: (الدولار = {EXCHANGE_RATE} ريال يمني).\n"
            f"• لخدمتك بشكل أسرع وتنفيذ طلبك بدقة، اضغط على زر التواصل أدناه وتواصل مباشرة مع الإدارة ({ADMIN_NAME}) لإرسال الرابط والكمية المطلوبة وستتم خدمتك فوراً!"
        )
        bot.edit_message_text(msg_text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "main_menu":
        user_id = call.from_user.id
        balance_yer = get_balance(user_id) * EXCHANGE_RATE
        
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("🛒 شراء أرقام وهمية وافتراضية مضمونة", callback_data="buy_number")
        )
        row2_1 = InlineKeyboardButton("💬 عروض WhatsApp", callback_data="offers_wa")
        row2_2 = InlineKeyboardButton("✈️ عروض Telegram", callback_data="offers_tg")
        markup.row(row2_1, row2_2)
        
        row3_1 = InlineKeyboardButton("🎲 شحن الرصيد", callback_data="wallet")
        row3_2 = InlineKeyboardButton("🎳 الأكثر طلباً وتوفراً", callback_data="most_used")
        markup.row(row3_1, row3_2)
        
        markup.add(
            InlineKeyboardButton("🚀 رشق جميع منصات التواصل الاجتماعي (SMM)", callback_data="services")
        )
        
        row5_1 = InlineKeyboardButton("📞 التواصل مع الإدارة", url=f"tg://resolve?domain={ADMIN_USERNAME}")
        row5_2 = InlineKeyboardButton("🛠️ الدعم الفني", url=f"tg://resolve?domain={ADMIN_USERNAME}")
        markup.row(row5_1, row5_2)
        
        markup.add(
            InlineKeyboardButton("📖 تعليمات وطريقة استخدام البوت", callback_data="help"),
            InlineKeyboardButton("👤 حسابي الشخصي", callback_data="account")
        )
        
        bot.edit_message_text(
            f"👤 الآيدي: {user_id}\n"
            f"💙 رصيدك الحالي: {balance_yer:,.0f} ريال يمني\n\n"
            f"━━━━━━━━━━━━━━━\n\n"
            f"🔥 أهلاً بك في منصتك الاحترافية الأولى والأسرع!\n\n"
            f"💎 نبذة عنا:\n"
            f"نحن بوابتك الموثوقة لخدمات الرشق المتكاملة لجميع وسائل التواصل الاجتماعي، وتوفير الأرقام الوهمية والافتراضية بأعلى جودة وضمانة حصرية.\n"
            f"🛡️ موثق ومعتمد من شركة SMM العالمية لضمان السرعة والأمان!\n\n"
            f"👇 اختر ما يناسبك من القائمة أدناه:",
            call.message.chat.id, 
            call.message.message_id, 
            reply_markup=markup
        )

if __name__ == '__main__':
    t = Thread(target=run_web)
    t.start()
    
    print("SMM Pro Bot is starting successfully...")
    while True:
        try:
            bot.remove_webhook()
            bot.infinity_polling(skip_pending=True, timeout=90, long_polling_timeout=60)
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(5)
