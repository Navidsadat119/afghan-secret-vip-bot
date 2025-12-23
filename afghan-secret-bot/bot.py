# bot.py
import telebot
from telebot import types
import json
import os
import time
import threading

# ================== CONFIG ==================
TOKEN = os.environ.get("8283730101:AAGk-tjB27nAEDw3BR7Cb-xQ2CvxGKOBEiU")  # توکن ربات از Environment Variable خوانده می‌شود

CHANNEL = "@afg_secret_team"
GROUP = "@afghan_secret_Group"

ADMIN_ID = 7672260551
ADMIN_USERNAME = "@Navid_Jan_Sadat"

LINK_BUY_NUMBER = "https://t.me/VirtualNumber_AF_bot?start=7672260551"
LINK_CAMERA = "https://t.me/Camera_HkBot"
LINK_SOCIAL_HACK = "https://t.me/VIP_H4CK_BOT?start=Bot53643923"
LINK_FREENET = "https://t.me/afghan_secret_freenet"
LINK_MUSIC = "https://t.me/Kali_Music_BOT"
LINK_FREE_NUMBER = "https://t.me/Online_Number_Bot"
LINK_FREE_EMAIL = "https://t.me/OnlineEmailBot"
LINK_IMAGE = "https://t.me/IMGEnhancer_Bot?start=7672260551"

WHATSAPP = "https://wa.me/93765305653"
# ============================================

DATA_FILE = "data.json"

DEFAULT_DATA = {
    "users": {},
    "ref_by": {},
    "daily_new": 0
}

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump(DEFAULT_DATA, f)
        return DEFAULT_DATA.copy()
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    for k in DEFAULT_DATA:
        if k not in data:
            data[k] = DEFAULT_DATA[k]
    return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

bot = telebot.TeleBot(TOKEN)
data = load_data()

# ================== HELPERS ==================
def is_joined(uid):
    try:
        c = bot.get_chat_member(CHANNEL, uid).status
        g = bot.get_chat_member(GROUP, uid).status
        return c in ["member", "administrator", "creator"] and g in ["member", "administrator", "creator"]
    except:
        return False

def user(uid):
    uid = str(uid)
    if uid not in data["users"]:
        data["users"][uid] = {
            "coins": 0,
            "invites": 0
        }
        data["daily_new"] += 1
        save_data(data)
    return data["users"][uid]

def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📱 خرید شماره مجازی")
    kb.row("🌐 آموزش نت رایگان 🔒", "📞 شماره مجازی رایگان 🔒")
    kb.row("🔐 هک صفحات اجتماعی 🔒", "📷 هک کامره")
    kb.row("🎵 موزیک‌یاب", "📧 ایمیل مجازی رایگان")
    kb.row("🖼️ شفاف‌ساز عکس")
    kb.row("⭐ جمع‌کردن سکه", "🆘 پشتیبانی")
    return kb

# ================== START ==================
@bot.message_handler(commands=["start"])
def start(m):
    uid = m.from_user.id
    args = m.text.split()

    user(uid)

    # referral
    if len(args) > 1:
        ref = args[1]
        if ref != str(uid) and ref not in data["ref_by"]:
            data["ref_by"][str(uid)] = ref
            if ref in data["users"]:
                data["users"][ref]["coins"] += 1
                data["users"][ref]["invites"] += 1
                try:
                    bot.send_message(
                        int(ref),
                        f"🎉 یک نفر با لینک تو آمد!\n⭐ سکه فعلی: {data['users'][ref]['coins']}"
                    )
                except:
                    pass
            save_data(data)

    if not is_joined(uid):
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton("📢 کانال", url=CHANNEL),
            types.InlineKeyboardButton("👥 گروپ", url=GROUP)
        )
        kb.add(types.InlineKeyboardButton("✅ بررسی عضویت", callback_data="check"))
        bot.send_message(
            m.chat.id,
            "⚠️ برای استفاده از ربات باید عضو کانال و گروپ شوی.",
            reply_markup=kb
        )
        return

    bot.send_message(
        m.chat.id,
        "👋 خوش آمدی به ربات رسمی Afghan Secret Team\n\n"
        "⭐ با دعوت دوستان سکه بگیر\n"
        "🔓 قفل امکانات را باز کن\n"
        "🎁 جایزه ویژه برای دعوت‌های زیاد",
        reply_markup=main_menu()
    )

@bot.callback_query_handler(func=lambda c: c.data == "check")
def check(c):
    if is_joined(c.from_user.id):
        bot.answer_callback_query(c.id, "✅ تایید شد")
        bot.send_message(c.message.chat.id, "وارد شدی 👇", reply_markup=main_menu())
    else:
        bot.answer_callback_query(c.id, "❌ هنوز عضو نیستی", show_alert=True)

# ================== FEATURES ==================
@bot.message_handler(func=lambda m: m.text == "⭐ جمع‌کردن سکه")
def coins(m):
    uid = str(m.from_user.id)
    link = f"https://t.me/{bot.get_me().username}?start={uid}"
    u = user(uid)
    bot.send_message(
        m.chat.id,
        f"⭐ سکه‌های تو: {u['coins']}\n"
        f"👥 دعوت‌ها: {u['invites']}\n\n"
        f"🔗 لینک دعوت:\n{link}\n\n"
        "هر دعوت = 1 ⭐"
    )

def locked(m, need, text, link):
    u = user(m.from_user.id)
    if u["coins"] < need:
        bot.send_message(
            m.chat.id,
            f"🔒 قفل است!\n⭐ لازم: {need}\n⭐ فعلی: {u['coins']}"
        )
    else:
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🚀 ادامه", url=link))
        bot.send_message(m.chat.id, text, reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "🌐 آموزش نت رایگان 🔒")
def freenet(m):
    locked(
        m, 5,
        "🌐 آموزش نت رایگان\nATOMA • Etisalat • Roshan",
        LINK_FREENET
    )

@bot.message_handler(func=lambda m: m.text == "📞 شماره مجازی رایگان 🔒")
def free_num(m):
    locked(
        m, 10,
        "📞 شماره مجازی رایگان\n🌍 همه کشورها\n⚡ دریافت سریع کد",
        LINK_FREE_NUMBER
    )

@bot.message_handler(func=lambda m: m.text == "🔐 هک صفحات اجتماعی 🔒")
def hack(m):
    locked(
        m, 10,
        "🔐 هک صفحات اجتماعی\nTelegram • WhatsApp • Gallery",
        LINK_SOCIAL_HACK
    )

@bot.message_handler(func=lambda m: m.text == "📱 خرید شماره مجازی")
def buy(m):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("💬 پیام به ادمین", url=f"https://t.me/{ADMIN_USERNAME[1:]}"))
    bot.send_message(
        m.chat.id,
        "📱 شماره‌های دایمی و قوی\nواتساپ آماده\nپرداخت مستقیم",
        reply_markup=kb
    )

@bot.message_handler(func=lambda m: m.text == "📷 هک کامره")
def cam(m):
    bot.send_message(m.chat.id, "📷 ابزار هک کامره", reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("ادامه", url=LINK_CAMERA)
    ))

@bot.message_handler(func=lambda m: m.text == "🎵 موزیک‌یاب")
def music(m):
    bot.send_message(m.chat.id, "🎵 موزیک‌یاب حرفه‌ای", reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("باز کردن", url=LINK_MUSIC)
    ))

@bot.message_handler(func=lambda m: m.text == "📧 ایمیل مجازی رایگان")
def email(m):
    bot.send_message(m.chat.id, "📧 ایمیل مجازی رایگان", reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("باز کردن", url=LINK_FREE_EMAIL)
    ))

@bot.message_handler(func=lambda m: m.text == "🖼️ شفاف‌ساز عکس")
def img(m):
    bot.send_message(m.chat.id, "🖼️ شفاف‌سازی و بهبود عکس", reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("باز کردن", url=LINK_IMAGE)
    ))

@bot.message_handler(func=lambda m: m.text == "🆘 پشتیبانی")
def sup(m):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("تلگرام", url=f"https://t.me/{ADMIN_USERNAME[1:]}"))
    kb.add(types.InlineKeyboardButton("واتساپ", url=WHATSAPP))
    bot.send_message(m.chat.id, "🆘 پشتیبانی", reply_markup=kb)

# ================== DAILY REPORT ==================
def daily_report():
    while True:
        time.sleep(86400)
        try:
            msg = (
                "📊 گزارش روزانه\n\n"
                f"👤 کاربران: {len(data['users'])}\n"
                f"➕ جدید امروز: {data['daily_new']}"
            )
            bot.send_message(ADMIN_ID, msg)
            data["daily_new"] = 0
            save_data(data)
        except:
            pass

threading.Thread(target=daily_report, daemon=True).start()

bot.infinity_polling()
def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump(DEFAULT_DATA, f)
        return DEFAULT_DATA.copy()
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    for k in DEFAULT_DATA:
        if k not in data:
            data[k] = DEFAULT_DATA[k]
    return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

bot = telebot.TeleBot(TOKEN)
data = load_data()

# ================== HELPERS ==================
def is_joined(uid):
    try:
        c = bot.get_chat_member(CHANNEL, uid).status
        g = bot.get_chat_member(GROUP, uid).status
        return c in ["member", "administrator", "creator"] and g in ["member", "administrator", "creator"]
    except:
        return False

def user(uid):
    uid = str(uid)
    if uid not in data["users"]:
        data["users"][uid] = {
            "coins": 0,
            "invites": 0
        }
        data["daily_new"] += 1
        save_data(data)
    return data["users"][uid]

def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📱 خرید شماره مجازی")
    kb.row("🌐 آموزش نت رایگان 🔒", "📞 شماره مجازی رایگان 🔒")
    kb.row("🔐 هک صفحات اجتماعی 🔒", "📷 هک کامره")
    kb.row("🎵 موزیک‌یاب", "📧 ایمیل مجازی رایگان")
    kb.row("🖼️ شفاف‌ساز عکس")
    kb.row("⭐ جمع‌کردن سکه", "🆘 پشتیبانی")
    return kb

# ================== START ==================
@bot.message_handler(commands=["start"])
def start(m):
    uid = m.from_user.id
    args = m.text.split()

    user(uid)

    # referral
    if len(args) > 1:
        ref = args[1]
        if ref != str(uid) and ref not in data["ref_by"]:
            data["ref_by"][str(uid)] = ref
            if ref in data["users"]:
                data["users"][ref]["coins"] += 1
                data["users"][ref]["invites"] += 1
                try:
                    bot.send_message(
                        int(ref),
                        f"🎉 یک نفر با لینک تو آمد!\n⭐ سکه فعلی: {data['users'][ref]['coins']}"
                    )
                except:
                    pass
            save_data(data)

    if not is_joined(uid):
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton("📢 کانال", url="https://t.me/afg_secret_team"),
            types.InlineKeyboardButton("👥 گروپ", url="https://t.me/afghan_secret_Group")
        )
        kb.add(types.InlineKeyboardButton("✅ بررسی عضویت", callback_data="check"))
        bot.send_message(
            m.chat.id,
            "⚠️ برای استفاده از ربات باید عضو کانال و گروپ شوی.",
            reply_markup=kb
        )
        return

    bot.send_message(
        m.chat.id,
        "👋 خوش آمدی به ربات رسمی Afghan Secret Team\n\n"
        "⭐ با دعوت دوستان سکه بگیر\n"
        "🔓 قفل امکانات را باز کن\n"
        "🎁 جایزه ویژه برای دعوت‌های زیاد",
        reply_markup=main_menu()
    )

@bot.callback_query_handler(func=lambda c: c.data == "check")
def check(c):
    if is_joined(c.from_user.id):
        bot.answer_callback_query(c.id, "✅ تایید شد")
        bot.send_message(c.message.chat.id, "وارد شدی 👇", reply_markup=main_menu())
    else:
        bot.answer_callback_query(c.id, "❌ هنوز عضو نیستی", show_alert=True)

# ================== FEATURES ==================
@bot.message_handler(func=lambda m: m.text == "⭐ جمع‌کردن سکه")
def coins(m):
    uid = str(m.from_user.id)
    link = f"https://t.me/{bot.get_me().username}?start={uid}"
    u = user(uid)
    bot.send_message(
        m.chat.id,
        f"⭐ سکه‌های تو: {u['coins']}\n"
        f"👥 دعوت‌ها: {u['invites']}\n\n"
        f"🔗 لینک دعوت:\n{link}\n\n"
        "هر دعوت = 1 ⭐"
    )

def locked(m, need, text, link):
    u = user(m.from_user.id)
    if u["coins"] < need:
        bot.send_message(
            m.chat.id,
            f"🔒 قفل است!\n⭐ لازم: {need}\n⭐ فعلی: {u['coins']}"
        )
    else:
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🚀 ادامه", url=link))
        bot.send_message(m.chat.id, text, reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "🌐 آموزش نت رایگان 🔒")
def freenet(m):
    locked(
        m, 5,
        "🌐 آموزش نت رایگان\nATOMA • Etisalat • Roshan",
        LINK_FREENET
    )

@bot.message_handler(func=lambda m: m.text == "📞 شماره مجازی رایگان 🔒")
def free_num(m):
    locked(
        m, 10,
        "📞 شماره مجازی رایگان\n🌍 همه کشورها\n⚡ دریافت سریع کد",
        LINK_FREE_NUMBER
    )

@bot.message_handler(func=lambda m: m.text == "🔐 هک صفحات اجتماعی 🔒")
def hack(m):
    locked(
        m, 10,
        "🔐 هک صفحات اجتماعی\nTelegram • WhatsApp • Gallery",
        LINK_SOCIAL_HACK
    )

@bot.message_handler(func=lambda m: m.text == "📱 خرید شماره مجازی")
def buy(m):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("💬 پیام به ادمین", url=f"https://t.me/{ADMIN_USERNAME[1:]}"))
    bot.send_message(
        m.chat.id,
        "📱 شماره‌های دایمی و قوی\nواتساپ آماده\nپرداخت مستقیم",
        reply_markup=kb
    )

@bot.message_handler(func=lambda m: m.text == "📷 هک کامره")
def cam(m):
    bot.send_message(m.chat.id, "📷 ابزار هک کامره", reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("ادامه", url=LINK_CAMERA)
    ))

@bot.message_handler(func=lambda m: m.text == "🎵 موزیک‌یاب")
def music(m):
    bot.send_message(m.chat.id, "🎵 موزیک‌یاب حرفه‌ای", reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("باز کردن", url=LINK_MUSIC)
    ))

@bot.message_handler(func=lambda m: m.text == "📧 ایمیل مجازی رایگان")
def email(m):
    bot.send_message(m.chat.id, "📧 ایمیل مجازی رایگان", reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("باز کردن", url=LINK_FREE_EMAIL)
    ))

@bot.message_handler(func=lambda m: m.text == "🖼️ شفاف‌ساز عکس")
def img(m):
    bot.send_message(m.chat.id, "🖼️ شفاف‌سازی و بهبود عکس", reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("باز کردن", url=LINK_IMAGE)
    ))

@bot.message_handler(func=lambda m: m.text == "🆘 پشتیبانی")
def sup(m):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("تلگرام", url=f"https://t.me/{ADMIN_USERNAME[1:]}"))
    kb.add(types.InlineKeyboardButton("واتساپ", url=WHATSAPP))
    bot.send_message(m.chat.id, "🆘 پشتیبانی", reply_markup=kb)

# ================== DAILY REPORT (SAFE) ==================
def daily_report():
    while True:
        time.sleep(86400)
        try:
            msg = (
                "📊 گزارش روزانه\n\n"
                f"👤 کاربران: {len(data['users'])}\n"
                f"➕ جدید امروز: {data['daily_new']}"
            )
            bot.send_message(ADMIN_ID, msg)
            data["daily_new"] = 0
            save_data(data)
        except:
            pass

threading.Thread(target=daily_report, daemon=True).start()

bot.infinity_polling()
