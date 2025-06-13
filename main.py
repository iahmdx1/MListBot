import telebot
import os

# استبدل هذا بالـ Token الخاص بـ Bot الخاص بك
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
user_list = {}  # قاموس لتخزين المستخدمين مع معرفات الدردشة الخاصة بهم

# أزرار تسجيل الدخول والخروج
login_button = telebot.types.InlineKeyboardButton(text="Log In 🟢", callback_data="login")
logout_button = telebot.types.InlineKeyboardButton(text="Log Out 🔴", callback_data="logout")
login_markup = telebot.types.InlineKeyboardMarkup([[login_button, logout_button]])

# معالج الأوامر /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "اضغط على الزر لتسجيل الدخول أو الخروج:", reply_markup=login_markup)

# معالج لزر تسجيل الدخول
@bot.callback_query_handler(func=lambda call: call.data == 'login')
def login_callback(call):
    user_id = call.from_user.id
    username = call.from_user.username or call.from_user.first_name
    chat_id = call.message.chat.id
    message_thread_id = call.message.message_thread_id if call.message.is_topic_message else None

    if user_id not in user_list:
        user_list[user_id] = {'username': username, 'chat_id': chat_id, 'message_thread_id': message_thread_id}
        bot.answer_callback_query(call.id, "تم تسجيل دخولك!")
    else:
        bot.answer_callback_query(call.id, "أنت مسجل بالفعل!")

# معالج لزر تسجيل الخروج
@bot.callback_query_handler(func=lambda call: call.data == 'logout')
def logout_callback(call):
    user_id = call.from_user.id
    if user_id in user_list:
        del user_list[user_id]
        bot.answer_callback_query(call.id, "تم تسجيل خروجك!")
    else:
        bot.answer_callback_query(call.id, "أنت غير مسجل!")

# معالج الأوامر /in لتسجيل الدخول
@bot.message_handler(commands=['in'])
def in_command(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    chat_id = message.chat.id
    message_thread_id = message.message_thread_id if message.is_topic_message else None

    if user_id not in user_list:
        user_list[user_id] = {'username': username, 'chat_id': chat_id, 'message_thread_id': message_thread_id}
        bot.reply_to(message, "تم تسجيل دخولك!")
    else:
        bot.reply_to(message, "أنت مسجل بالفعل!")

# معالج الأوامر /out لتسجيل الخروج
@bot.message_handler(commands=['out'])
def out_command(message):
    user_id = message.from_user.id
    if user_id in user_list:
        del user_list[user_id]
        bot.reply_to(message, "تم تسجيل خروجك!")
    else:
        bot.reply_to(message, "أنت غير مسجل!")

# معالج الأوامر /mlist لعرض قائمة المستخدمين
@bot.message_handler(commands=['mlist'])
def mlist_command(message):
    chat_id = message.chat.id
    message_thread_id = message.message_thread_id if message.is_topic_message else None
    
    users_in_topic = [user['username'] for user_id, user in user_list.items()
                       if user['chat_id'] == chat_id and user['message_thread_id'] == message_thread_id]
    
    if users_in_topic:
        users = "\n".join(users_in_topic)
        bot.send_message(chat_id, f"المستخدمون المسجلون في هذا الموضوع:\n{users}", message_thread_id=message_thread_id)
    else:
        bot.send_message(chat_id, "لا يوجد مستخدمون مسجلون في هذا الموضوع حتى الآن.", message_thread_id=message_thread_id)

# تشغيل الـ Bot
bot.infinity_polling()
