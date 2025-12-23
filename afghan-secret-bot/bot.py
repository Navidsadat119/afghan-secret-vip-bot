import telebot
from telebot import types
import json, os, time, threading
from datetime import datetime

# ================== تنظیمات ==================
TOKEN = "8283730101:AAGk-tjB27nAEDw3BR7Cb-xQ2CvxGKOBEiU"

CHANNEL = "@afg_secret_team"
GROUP = "@afghan_secret_Group"

ADMIN_ID = 7672260551
ADMIN_USER = "@Navid_Jan_Sadat"

WHATSAPP = "0765305653"
WA_CHANNEL = "https://whatsapp.com/channel/0029VbCABcx7IUYUKglHgG2y"
WA_GROUP = "https://chat.whatsapp.com/GGcJB4W0t6vLMkfljHeBqF?mode=hqrt2"

LINKS = {
    "buy_vn": "https://t.me/VirtualNumber_AF_bot?start=7672260551",
    "camera": "https://t.me/Camera_HkBot",
    "hack": "https://t.me/VIP_H4CK_BOT?start=Bot53643923",
    "net": "https://t.me/afghan_secret_freenet",
    "music": "https://t.me/Kali_Music_BOT",
    "free_vn": "https://t.me/Online_Number_Bot",
    "email": "https://t.me/OnlineEmailBot",
    "img": "https://t.me/IMGEnhancer_Bot?start=7672260551"
}

DATA_FILE = "data.json"
# ============================================

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ---------- دیتابیس ----------
if os.path.exists(DATA_FILE):
    data = json.load(open(DATA_FILE))
else:
    data = {}

data.setdefault("users", {})
data.setdefault("ref", {})
data.setdefault("daily", {})

def save():
    json.dump(data, open(DATA_FILE, "w"), indent=2)

# ---------- عضویت ----------
def is_joined(uid):
    try:
        a = bot.get_chat_member(CHANNEL, uid).status
        b = bot.get_chat_member(GROUP, uid).status
        return a in ["member","administrator","creator"] and b in ["member","administrator","creator"]
    except:
        return False

# ---------- منوی اصلی ----------
def main_menu(chat_id, uid):
    coins = data["users"][str(uid)]["coins"]
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🌐 آموزش نت رایگان 🔒", "📱 شماره مجازی رایگان 🔒")
    kb.add("😈 هک صفحات اجتماعی 🔒", "📸 شفاف‌ساز عکس")
    kb.add("🎵 موزیک‌یاب", "📥 خرید شماره مجازی")
    kb.add("⭐ سکه‌های من", "🆘 پشتیبانی")

    bot.send_message(
        chat_id,
        f"""✨ <b>خوش آمدی!</b>

⭐ سکه‌های تو: <b>{coins}</b>

🔓 بازشدن قفل‌ها:
• 5 ⭐ نت رایگان
• 10 ⭐ هک صفحات
• 10 ⭐ شماره مجازی رایگان

👥 هر دعوت = 1 سکه
🎁 جایزه ویژه برای فعال‌ها

ساخته شده توسط <b>Afghan Secret Team</b> 🖤""",
        reply_markup=kb
    )

# ---------- START ----------
@bot.message_handler(commands=["start"])
def start(m):
    uid = str(m.from_user.id)

    if uid not in data["users"]:
        data["users"][uid] = {"coins": 0}
        save()

    args = m.text.split()
    if len(args) > 1:
        ref = args[1]
        if ref != uid and ref in data["users"]:
            if uid not in data["ref"].get(ref, []):
                data["ref"].setdefault(ref, []).append(uid)
                data["users"][ref]["coins"] += 1
                save()
                bot.send_message(int(ref), "🎉 یک نفر با لینک تو آمد! +1 ⭐")

    if not is_joined(int(uid)):
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton("📢 کانال", url="https://t.me/afg_secret_team"),
            types.InlineKeyboardButton("👥 گروه", url="https://t.me/afghan_secret_Group")
        )
        kb.add(types.InlineKeyboardButton("✅ بررسی عضویت", callback_data="check"))
        bot.send_message(m.chat.id,
            "⚠️ برای استفاده باید عضو کانال و گروه شوی 👇",
            reply_markup=kb
        )
        return

    main_menu(m.chat.id, int(uid))

# ---------- بررسی عضویت ----------
@bot.callback_query_handler(func=lambda c: c.data=="check")
def check(c):
    if is_joined(c.from_user.id):
        main_menu(c.message.chat.id, c.from_user.id)
    else:
        bot.answer_callback_query(c.id, "❌ هنوز عضو نیستی", show_alert=True)

# ---------- قفل‌ها ----------
def locked(m, need):
    uid = str(m.from_user.id)
    coins = data["users"][uid]["coins"]
    if coins < need:
        bot.send_message(m.chat.id,
            f"🔒 قفل است!\n\nنیاز: {need} ⭐\nسکه تو: {coins} ⭐\n\n👥 با دعوت سکه بگیر یا از ادمین بخر 🫰")
        return True
    data["users"][uid]["coins"] -= need
    save()
    return False

@bot.message_handler(func=lambda m: m.text=="🌐 آموزش نت رایگان 🔒")
def net(m):
    if locked(m,5): return
    bot.send_message(m.chat.id,
        "🌐 آموزش نت رایگان فعال شد!\n📶 ATOMA\n📶 Etisalat\n📶 Roshan\n\n👇",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("مشاهده آموزش", url=LINKS["net"])
        )
    )

@bot.message_handler(func=lambda m: m.text=="📱 شماره مجازی رایگان 🔒")
def free_vn(m):
    if locked(m,10): return
    bot.send_message(m.chat.id,
        "📱 شماره مجازی رایگان\n🌍 تمام کشورها\n⚡ دریافت سریع کد",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("دریافت", url=LINKS["free_vn"])
        )
    )

@bot.message_handler(func=lambda m: m.text=="😈 هک صفحات اجتماعی 🔒")
def hack(m):
    if locked(m,10): return
    bot.send_message(m.chat.id,
        "😈 ابزار هک صفحات\n• تلگرام\n• واتساپ\n• گالری\n• مخاطبین\n\nساخته شده توسط king zabi",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("ورود", url=LINKS["hack"])
        )
    )

# ---------- آزاد ----------
@bot.message_handler(func=lambda m: m.text=="📸 شفاف‌ساز عکس")
def img(m):
    bot.send_message(m.chat.id,"📸 بهبود چهره و کیفیت عکس 👇",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("باز کردن", url=LINKS["img"])
        ))

@bot.message_handler(func=lambda m: m.text=="🎵 موزیک‌یاب")
def music(m):
    bot.send_message(m.chat.id,"🎵 موزیک‌یاب هوشمند 👇",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("باز کردن", url=LINKS["music"])
        ))

@bot.message_handler(func=lambda m: m.text=="📥 خرید شماره مجازی")
def buy(m):
    bot.send_message(m.chat.id,"📥 خرید شماره مجازی دایمی 👇",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("خرید", url=LINKS["buy_vn"])
        ))

@bot.message_handler(func=lambda m: m.text=="⭐ سکه‌های من")
def coins(m):
    uid=str(m.from_user.id)
    bot.send_message(m.chat.id,
        f"⭐ سکه‌های تو: {data['users'][uid]['coins']}\n\n👥 هر دعوت = 1 سکه\n💬 خرید سکه: @{ADMIN_USER[1:]}")

@bot.message_handler(func=lambda m: m.text=="🆘 پشتیبانی")
def sup(m):
    kb=types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("تلگرام", url=f"https://t.me/{ADMIN_USER[1:]}"))
    kb.add(types.InlineKeyboardButton("واتساپ", url=f"https://wa.me/93{WHATSAPP}"))
    kb.add(types.InlineKeyboardButton("کانال واتساپ", url=WA_CHANNEL))
    kb.add(types.InlineKeyboardButton("گروه واتساپ", url=WA_GROUP))
    bot.send_message(m.chat.id,"🆘 پشتیبانی 👇",reply_markup=kb)

# ---------- گزارش روزانه ----------
def daily_report():
    while True:
        time.sleep(86400)
        users=len(data["users"])
        coins=sum(u["coins"] for u in data["users"].values())
        bot.send_message(ADMIN_ID,
            f"📊 گزارش روزانه\n👤 کاربران: {users}\n⭐ مجموع سکه‌ها: {coins}")

threading.Thread(target=daily_report, daemon=True).start()

# ---------- اجرا ----------
bot.infinity_polling()
