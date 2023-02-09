# Тима Минский tg: https://t.me/tima_minski
# главная ветка проекта, handler и прочие обработки

from config import text_start, info_text,dt, fs
from keyboards import start_keyboard, return_keyboard
from loader import bot
from admin_functionality.statistics_admin import handler_statistic
from admin_functionality.ban_message import bot
from admin_functionality.ban_words import handler_ban_words
from admin_functionality.add_del_admin_user import bot

@bot.message_handler(chat_types=['private'], commands=['stst'])
def change_profile(message):
    name = message.from_user.first_name
    user_id = message.from_user.id

    bot.send_message(message.chat.id, f'Hello , <b>{name}</b> ! ☺️ \n' 
                     f' Ты можешь изменить свою карточку пользователя! \n', parse_mode="html")

@bot.message_handler(chat_types=['private'],commands=['start'])
def start(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    bot.send_message(message.chat.id, f'Hello , <b>{name}</b> ! ☺️', parse_mode="html")
    bot.send_message(message.chat.id, text_start, parse_mode='Markdown', disable_web_page_preview=True,
                     reply_markup=start_keyboard(user_id))



@bot.callback_query_handler(func=lambda call: True)
def call(call):
    idx = call.message.chat.id
    user_id = call.message.chat.id
    data = dt(call.data)
    flag = fs(call.data)
    handler_statistic(call)  # на кнопку статистика в главном меню бота
    handler_ban_words(call)  #  на кнопку добавить бан слова
    # Флаг для выброса информации кнопка "Инфо"
    if flag == 'in':
        info = "info"
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text=info_text, reply_markup=return_keyboard(info), parse_mode='Markdown',
                              disable_web_page_preview=True)

    # Флаг для возврата в меню, кнопки "выход", "Все понятно"
    if flag == "ss":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, text_start,
                         reply_markup=start_keyboard(user_id),parse_mode='Markdown',
                                      disable_web_page_preview=True)






















print("Ready")
bot.infinity_polling()