hereimport telebot
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

# مفتاح الـ API الخاص بك وموقع SMMKings
API_KEY = "2eabc2491e6edcdeeac47c9090e02a96"
API_URL = "https://smmkings.com/api/v2"

# سعر الصرف المعتمد: 1 دولار = 800 ريال يمني
EXCHANGE_RATE = 800

bot = telebot.TeleBot(TOKEN)
user_balances = {}

# سيرفر الويب الوهمي للحفاظ على العلامة الزرقاء في Render
app = Flask('')

@app.route('/')
def home():
    return "SMM Pro API Bot is running and active!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def get_balance(user_id):
    return user_balances.get(user_id, 0.0)

def update_balance(user_id, amount):
    user_balances[user_id] = get_balance(user_id) + amount

# دالة لجلب الخدمات من الموقع عبر الـ API
def get_smm_services():
    try:
        response = requests.post(API_URL, data={
            'key': API_KEY,
            'action': 'services'
        }, timeout=10)
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
    
    row2_1 = InlineKeyboardButton("💬 خدمات WhatsApp الشاملة", callback_data="serv_whatsapp")
    row2_2 = InlineKeyboardButton("✈️ خدمات Telegram الشاملة", callback_data="serv_telegram")
    markup.row(row2_1, row2_2)
    
    row3_1 = InlineKeyboardButton("🎲 شحن الرصيد", callback_data="wallet")
    row3_2 = InlineKeyboardButton("🎳 الأكثر طلباً وتوفراً", callback_data="most_used")
    markup.row(row3_1, row3_2)
    
    markup.add(
        InlineKeyboardButton("🚀 عرض جميع خدمات الموقع (مباشرة عبر الـ API)", callback_data="fetch_api_services")
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
        f"🔥 أهلاً بك في منصتك الاحترافية المربوطة بموقع SMMKINGS!\n\n"
        f"💎 نبذة عنا:\n"
        f"نوفر لك جميع خدمات الرشق والاتصال والواتساب والتليجرام مباشرة بأسعار مميزة محسوبة بالريال اليمني (الدولار = {EXCHANGE_RATE} ريال).\n\n"
        f"👇 اختر ما يناسبك من القائمة أدناه:",
        reply_markup=markup
    )

@bot.message_handler(commands=['addbalance'])
def add_balance_cmd(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "عذراً، هذا الأمر مخصص للإدارة فقط.")
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(message, "⚠️ خطأ! استخدم الصيغة الصحيحة:\n`/addbalance user_id amount_in_usd`", parse_mode="Markdown")
        return
    
    try:
        target_user_id = int(args[1])
        amount_usd = float(args[2])
        amount_yer = amount_usd * EXCHANGE_RATE
        update_balance(target_user_id, amount_usd)
        
        bot.reply_to(message, f"✅ تم بنجاح إضافة `{amount_usd}$` (تقابله `{amount_yer:,.0f} ريال`) إلى رصيد المستخدم `{target_user_id}`.", parse_mode="Markdown")
        bot.send_message(target_user_id, f"🎉 تم شحن رصيدك بمبلغ `{amount_yer:,.0f} ريال يمني` بنجاح بواسطة الإدارة ({ADMIN_NAME})!", parse_mode="Markdown")
    except ValueError:
        bot.reply_to(message, "⚠️ تأكد من أن الآيدي والمبلغ أرقام صحيحة.")

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
        balance_yer = get_balance(user_id) * EXCHANGE_Rate if 'EXCHANGE_Rate' in globals() else get_balance(user_id) * EXCHANGE_RATE
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        bot.edit_message_text(f"👤 معلومات حسابك الشخصي:\n\n🆔 الآيدي الخاص بك: {user_id}\n💰 الرصيد المتاح: {balance_yer:,.0f} ريال يمني\n👨‍💼 المسؤول: {ADMIN_NAME}", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "fetch_api_services":
        bot.edit_message_text("🔄 جاري جلب جميع الخدمات المحدثة من موقع SMMKings...", call.message.chat.id, call.message.message_id)
        services = get_smm_services()
        
        if services and isinstance(services, list):
            # نعرض أول 15 خدمة كمثال مباشر مع حساب الأسعار بالريال اليمني
            text = "🚀 **أبرز الخدمات المتاحة حالياً من الموقع (محدثة تلقائياً):**\n\n"
            markup = InlineKeyboardMarkup(row_width=1)
            
            count = 0
            for s in services[:15]:  # عرض عينة أولية لتجنب طول الرسالة
                s_id = s.get('service')
                s_name = s.get('name')
                s_rate_usd = float(s.get('rate', 0))
                s_rate_yer = s_rate_usd * EXCHANGE_RATE
                
                text += f"🔹 **{s_name}**\n💰 السعر لكل 1000: ` {s_rate_yer:,.0f} ريال ` (رقم الخدمة: `{s_id}`)\n\n"
            
            markup.add(InlineKeyboardButton("📞 لطلب أي خدمة وتثبيتها، اضغط هنا", url=f"tg://resolve?domain={ADMIN_USERNAME}"))
            markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
            
            try:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            except Exception:
                # في حال كانت الرسالة طويلة جداً يتم عرض خيار التواصل المباشر
                bot.edit_message_text("✅ تم الاتصال بموقع SMMKings بنجاح وجلب كافة الخدمات.\n\nلطلب أي خدمة فوراً، تواصل مع الإدارة مباشرة:", call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
            bot.edit_message_text("⚠️ تعذر جلب الخدمات حالياً من الـ API، يجدر التأكد من المفتاح أو التواصل مع الدعم الفني.", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data in ["serv_whatsapp", "serv_telegram", "buy_number", "offers_whatsapp", "offers_telegram", "most_used", "help"]:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📞 التواصل مع الإدارة لتنفيذ الطلب فوراً", url=f"tg://resolve?domain={ADMIN_USERNAME}"))
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu"))
        
        msg_text = (
            f"🌟 قسم الخدمات المميزة والربط التلقائي (SMM):\n\n"
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
        row2_1 = InlineKeyboardButton("💬 خدمات WhatsApp الشاملة", callback_data="serv_whatsapp")
        row2_2 = InlineKeyboardButton("✈️ خدمات Telegram الشاملة", callback_data="serv_telegram")
        markup.row(row2_1, row2_2)
        
        row3_1 = InlineKeyboardButton("🎲 شحن الرصيد", callback_data="wallet")
        row3_2 = InlineKeyboardButton("🎳 الأكثر طلباً وتوفراً", callback_data="most_used")
        markup.row(row3_1, row3_2)
        
        markup.add(
            InlineKeyboardButton("🚀 عرض جميع خدمات الموقع (مباشرة عبر الـ API)", callback_data="fetch_api_services")
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
            f"🔥 أهلاً بك في منصتك الاحترافية المربوطة بموقع SMMKINGS!\n\n"
            f"💎 نبذة عنا:\n"
            f"نوفر لك جميع خدمات الرشق والاتصال والواتساب والتليجرام مباشرة بأسعار مميزة محسوبة بالريال اليمني (الدولار = {EXCHANGE_RATE} ريال).\n\n"
            f"👇 اختر ما يناسبك من القائمة أدناه:",
            call.message.chat.id, 
            call.message.message_id, 
            reply_markup=markup
        )

if __name__ == '__main__':
    t = Thread(target=run_web)
    t.start()
    
    print("SMM Pro API Bot is starting successfully...")
    while True:
        try:
            bot.remove_webhook()
            bot.infinity_polling(skip_pending=True, timeout=90, long_polling_timeout=60)
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(5)
