# Тима Минский tg: https://t.me/tima_minski
# главная ветка проекта, handler и прочие обработки
import json

import telebot
from config import bot, text_start,id_bot,name_bot,loser_text,info_text
from service_functions import dt, fs,check_is_group,check_is_admin,check_is_user,check_del_user
from keyboards import start_keyboard,statistics_keyboard,return_keyboard



@bot.message_handler(commands=['change_profile'])
def change_profile(message):
    name = message.from_user.first_name
    user_id = message.from_user.id

    bot.send_message(message.chat.id, f'Hello , <b>{name}</b> ! ☺️ \n' 
                     f' Ты можешь изменить свою карточку пользователя! \n', parse_mode="html")



# @bot.message_handler(content_types=['text'])
# def text (message):
#     bot.send_message(message.chat.id, "h")
#     print(message)



@bot.message_handler(commands=['start'])
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

    print(f'user {user_id}')

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

    # флаг для выброса статистики по активным группам владельца из файла "id.json"
# директория "administrator"
    if flag == 'st':
        num = 'statist'
        if data[0] =="*":
            page = int(data[1])
            user_id = data[2:]
            try:
                with open("administrator/" + str(user_id) + ".json", 'r', encoding='utf-8') as f:
                    buf_admin_file = json.loads(f.read())
                f.close()
                statistic = buf_admin_file['group']
                print(statistic)
                if len(statistic) > 0:
                    print("длина больше")
                    bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                          text="👥 <b>Выберете группу.</b>\nстраница - " + str(page+1),
                                          reply_markup=statistics_keyboard(statistic,page,user_id),parse_mode='html')
                else:
                    print("else")
                    bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                          text=loser_text, reply_markup=return_keyboard(num), parse_mode='Markdown',
                                          disable_web_page_preview=True)
            except Exception:
                print(Exception)
                bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                      text=loser_text, reply_markup=return_keyboard(num), parse_mode='Markdown',
                                      disable_web_page_preview=True)
        if data[0] == ":":
            print(data[0])
            try:
                bot.send_message(idx, "good")
                                 # reply_markup=card_view_keyboard(data[1:], "a")))
                # bot.send_message(call.message.chat.id, text_start,
                #                  reply_markup=start_keyboard(user_id))


            except:
                bot.send_message(call.message.chat.id, "Что-то пошло не так")





@bot.message_handler(content_types=["new_chat_members"])
def handler_new_member(message):
    group_title = message.chat.title # название группы
    group_id = message.chat.id # id группы
    new_user_id = message.new_chat_members[0].id
    new_user_name = message.new_chat_members[0].last_name
    if new_user_id == int(id_bot):
        check_is_group(group_id,group_title)# добавляет файл группы
    else:
        bot.send_message(message.chat.id, "Добро пожаловать, {0}!".format(new_user_name))
        check_is_user(message, group_id,new_user_id)

    check_is_admin(message, group_id)  # добавляет владельца


@bot.message_handler(content_types=['left_chat_member'])
def not_greeting(message):
    group_id = message.chat.id  # id группы
    print(message.left_chat_member.id)
    print("User " + message.left_chat_member.first_name + " left")
    try:
        if message.left_chat_member.id != int(id_bot):
            check_del_user(message, group_id)
        else:
            pass
    except OSError:
        pass


















print("Ready")
bot.infinity_polling()