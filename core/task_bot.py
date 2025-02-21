import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import threading
import time
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
SUPPORT_ID = os.getenv("SUPPORT_ID")

bot = telebot.TeleBot(TOKEN)

tasks = {}  

REPEAT_OPTIONS = {"بدون تکرار": "once", "روزانه": "daily", "هفتگی": "weekly", "ماهانه": "monthly"}

def check_subscription(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ["member", "administrator", "creator"]
    except:
        return False

@bot.message_handler(commands=["start"])
def start(message):
    channel_link = "https://t.me/task_mnl_frtn"
    if not check_subscription(message.from_user.id):
        bot.send_message(
            message.chat.id,
            f"برای استفاده از ربات لطفاً در کانال [این لینک]({channel_link}) عضو شوید.",
            parse_mode="Markdown"
        )
        return

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("افزودن وظیفه"), KeyboardButton("لیست وظایف"))
    markup.add(KeyboardButton("حذف وظیفه"), KeyboardButton("ارتباط با پشتیبانی"))

    bot.send_message(
        message.chat.id,
        "🎯 به ربات مدیریت وظایف خوش آمدید!\n"
        "با استفاده از این ربات می‌توانید وظایف خود را مدیریت کرده و یادآوری دریافت کنید.\n"
        "✅ ویژگی‌ها:\n"
        "- افزودن وظایف با زمانبندی دقیق\n"
        "- امکان تعیین تکرار روزانه، هفتگی یا ماهانه\n"
        "- مشاهده لیست وظایف ثبت شده\n"
        "- حذف وظایف در صورت نیاز\n"
        "- یادآوری خودکار وظایف در زمان مشخص شده\n"
        "\nدستورات:\n"
        "/addtask - افزودن وظیفه\n"
        "/mytasks - مشاهده لیست وظایف\n"
        "/removetask - حذف وظیفه\n"
        "/support - ارتباط با پشتیبانی",
        reply_markup=markup,
    )

@bot.message_handler(commands=["addtask"])
def add_task(message):
    if not check_subscription(message.from_user.id):
        bot.send_message(message.chat.id, "برای استفاده از ربات لطفاً در کانال عضو شوید.")
        return
    bot.send_message(message.chat.id, "📌 لطفاً وظیفه خود را ارسال کنید:")
    bot.register_next_step_handler(message, get_task_time)

def get_task_time(message):
    user_id = message.chat.id
    task_text = message.text
    bot.send_message(user_id, "⏰ لطفاً زمان یادآوری را به فرمت HH:MM وارد کنید:")
    bot.register_next_step_handler(message, lambda msg: process_time(msg, task_text))

def process_time(message, task_text):
    user_id = message.chat.id
    try:
        h, m = map(int, message.text.strip().split(":"))
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for option in REPEAT_OPTIONS:
            markup.add(KeyboardButton(option))
        bot.send_message(user_id, "🔁 لطفاً نوع تکرار را انتخاب کنید:", reply_markup=markup)
        bot.register_next_step_handler(message, lambda msg: save_task(msg, task_text, h, m))
    except:
        bot.send_message(user_id, "❌ فرمت نادرست! لطفاً زمان را صحیح وارد کنید.")

def save_task(message, task_text, h, m):
    user_id = message.chat.id
    repeat_type = REPEAT_OPTIONS.get(message.text, "once")
    tasks.setdefault(user_id, []).append((task_text, h, m, repeat_type))
    bot.send_message(user_id, f"✅ وظیفه '{task_text}' برای {h:02}:{m:02} با تکرار '{message.text}' تنظیم شد.")

def reminder_thread():
    while True:
        current_time = time.localtime()
        for user_id, user_tasks in list(tasks.items()):
            for task in list(user_tasks):
                task_text, h, m, repeat_type = task
                if current_time.tm_hour == h and current_time.tm_min == m:
                    bot.send_message(user_id, f"⏰ یادآوری: {task_text}")
                    if repeat_type == "once":
                        user_tasks.remove(task)
                    elif repeat_type == "weekly":
                        tasks[user_id].append((task_text, h, m, "weekly"))
                    elif repeat_type == "monthly":
                        tasks[user_id].append((task_text, h, m, "monthly"))
        time.sleep(60)

threading.Thread(target=reminder_thread, daemon=True).start()

@bot.message_handler(commands=["mytasks"])
def list_tasks(message):
    user_id = message.chat.id
    if user_id in tasks and tasks[user_id]:
        task_list = "\n".join([f"📌 {t[0]} - {t[1]:02}:{t[2]:02} ({t[3]})" for t in tasks[user_id]])
        bot.send_message(user_id, f"📝 لیست وظایف شما:\n{task_list}")
    else:
        bot.send_message(user_id, "✅ شما هیچ وظیفه‌ای ثبت نکرده‌اید.")

@bot.message_handler(commands=["removetask"])
def remove_task(message):
    user_id = message.chat.id
    if user_id not in tasks or not tasks[user_id]:
        bot.send_message(user_id, "❌ شما هیچ وظیفه‌ای ندارید.")
        return
    bot.send_message(user_id, "📌 لطفاً نام وظیفه‌ای که می‌خواهید حذف کنید ارسال کنید:")
    bot.register_next_step_handler(message, lambda msg: delete_task(msg, user_id))

def delete_task(message, user_id):
    task_name = message.text.strip()
    for task in tasks[user_id]:
        if task[0] == task_name:
            tasks[user_id].remove(task)
            bot.send_message(user_id, f"✅ وظیفه '{task_name}' حذف شد.")
            return
    bot.send_message(user_id, "❌ وظیفه موردنظر یافت نشد.")

bot.polling()
