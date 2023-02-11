import json
import threading
import time

from config import fs, dt
from loader import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def keyboard_statistic(group_id,val):
    keyboard = InlineKeyboardMarkup(row_width=2)
    button = InlineKeyboardButton("Просмотреть полностью", callback_data="s1" + str(group_id))
    button1 = InlineKeyboardButton("Свернуть", callback_data="s2" + str(group_id))
    button2 = InlineKeyboardButton("Авто оповещение", callback_data="s3" + str(group_id))
    button3 = InlineKeyboardButton("Назад", callback_data="st:" + str(group_id))
    button4 = InlineKeyboardButton("Выход", callback_data="ss" + str(group_id))
    button5 = InlineKeyboardButton("Интервал", callback_data="s4" + str(group_id))


    start = InlineKeyboardButton("Старт", callback_data="00++" + str(group_id))
    stop = InlineKeyboardButton("Стоп", callback_data="00--" + str(group_id))

    if val == "1":
        keyboard.add(button,button2,button3,button4)
    if val == "2":
        keyboard.add(button1,button2,button3,button4)
    if val == "3":
        keyboard.add(button5,button3,button4)
    if val == "4":
        keyboard.add(button2,button3,button4)
    if val == "5":
        keyboard.add(stop,button3,button4)
    if val == "6":
        keyboard.add(start,button3,button4)
    return keyboard


def statistic_group(call,group_id):
    val = "1"
    with open(f'groups/{str(group_id)}/{str(group_id)}.json', 'r', encoding='utf-8') as f:
        list = json.loads(f.read())
        f.close()
    with open(f'groups/{str(group_id)}/chat_history.json', 'r', encoding='utf-8') as h:
        list1 = json.loads(h.read())
        f.close()

        text = f'Название группы: {list["name_group"]}\n' \
               f'Владелец группы: {list["creator"]} \n' \
               f'Кол-во пользователей: {list["number_of_subscribers"]}\n' \
               f'Общее кол-во сообщений: {list1["number_message"]}\n' \

        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text= text,
                              reply_markup=keyboard_statistic(group_id,val), parse_mode='html')

def all_statistic_group(call,group_id):
    val = "2"
    with open(f'groups/{str(group_id)}/{str(group_id)}.json', 'r', encoding='utf-8') as f:
        list = json.loads(f.read())
        f.close()
    with open(f'groups/{str(group_id)}/chat_history.json', 'r', encoding='utf-8') as h:
        list1 = json.loads(h.read())
        f.close()
        text = f'Название группы: {list["name_group"]}\n' \
               f'Владелец группы: {list["creator"]} \n' \
               f'Кол-во пользователей: {list["number_of_subscribers"]}\n' \
               f'Кол-во удаленных пользователей: {list["subscribers_del_number"]}\n' \
               f'Общее кол-во сообщений: {list1["number_message"]}\n' \
               f'Кол-во пользователей в бан: {list["subscribers_ban_number"]}\n'

        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                      text=text,
                                      reply_markup=keyboard_statistic(group_id,val), parse_mode='html')

def stat_push(message,call,group_id):
    val = "6"
    with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
        list = json.loads(f.read())
        f.close()
    if message.content_type == ("text") and message.text.replace(" ", "") and message.text.isdigit():
        list["push_statistic"] = message.text

        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text='Нажмите Старт чтоб запустить автоматическую отправку\n'
                                   'Интервал оповещения каждые: ' + str(list["push_statistic"]) + ' минут.'
                              , reply_markup=keyboard_statistic(group_id,val),
                              parse_mode="Markdown", disable_web_page_preview=True)
        with open(f'groups/{str(group_id)}/push_notifications.json', "w", encoding="utf-8") as f:
            json.dump(list, f, ensure_ascii=False, indent=4)
            f.close()

    else:
        val = "4"
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text= '⚠️ Ошибка при вводе интервала! еще раз внимательно введи '
                                   'интервал в МИНУТАХ одним числом ⚠️'
                              , reply_markup=keyboard_statistic(group_id,val),
                              parse_mode="Markdown", disable_web_page_preview=True)
    bot.delete_message(message.chat.id, message.message_id)

def auto_push(call,group_id,time_):

    with open(f'groups/{str(group_id)}/{str(group_id)}.json', 'r', encoding='utf-8') as f:
        list = json.loads(f.read())
        f.close()
    with open(f'groups/{str(group_id)}/chat_history.json', 'r', encoding='utf-8') as h:
        list1 = json.loads(h.read())
        f.close()
        text = f'Название группы: {list["name_group"]}\n' \
               f'Владелец группы: {list["creator"]} \n' \
               f'Кол-во пользователей: {list["number_of_subscribers"]}\n' \
               f'Кол-во удаленных пользователей: {list["subscribers_del_number"]}\n' \
               f'Общее кол-во сообщений: {list1["number_message"]}\n' \
               f'Кол-во пользователей в бан: {list["subscribers_ban_number"]}\n'
    counter = 1
    while counter < 2:
        if thread_stop == True:
            print(counter)
            counter += 1
            time.sleep(0.5)

        bot.send_message(call.message.chat.id, text=text)
        time.sleep(time_)
def handler_statistic_group(call):
    data = dt(call.data)
    flag = fs(call.data)

    if flag == "s1":
        group_id = data
        all_statistic_group(call, group_id)

    if flag == "s2":
        group_id = data
        statistic_group(call, group_id)

    if flag == "s3":
        group_id = data
        with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
            list = json.load(f)
            f.close()
        if list["public_push_statistic"] == "yes":
            val = "5"
            bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                  text='⚠️Уведомление запущено⚠️\n',

                                  reply_markup=keyboard_statistic(group_id, val), parse_mode='Markdown',
                                  disable_web_page_preview=True)
        if list["public_push_statistic"] == "no":
            val = "3"
            message = bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                  text='⚠️Уведомление остановлено⚠️\n'
                                       'Укажите интервал чтоб запустить уведомление.',
                                  reply_markup=keyboard_statistic(group_id, val), parse_mode='Markdown',
                                  disable_web_page_preview=True)



    if flag =="00":
        control_notifications = data[:2]
        group_id = data[2:]
        global thread_stop
        if control_notifications =="++":
            val = "5"
            with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
                list = json.loads(f.read())
                f.close()
                list["public_push_statistic"] = "yes"
                bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                      text='Автоматическую отправка запущена\n'
                                           'Интервал оповещения каждые: ' + str(list["push_statistic"]) + ' минут.'
                                      , reply_markup=keyboard_statistic(group_id, val),
                                      parse_mode="Markdown", disable_web_page_preview=True)
            with open(f'groups/{str(group_id)}/push_notifications.json', "w", encoding="utf-8") as f:
                json.dump(list, f, ensure_ascii=False, indent=4)
                f.close()

            thread_stop = False
            thread = threading.Thread(target=auto_push,args=(call,group_id, int(list["push_statistic"])*60))
            thread.start()

        if control_notifications == "--":
            thread_stop = True #Присваеваем значение True и завершаем поток
            val = "3"
            with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
                list = json.loads(f.read())
                f.close()
                list["public_push_statistic"] = "no"
            with open(f'groups/{str(group_id)}/push_notifications.json', "w", encoding="utf-8") as f:
                json.dump(list, f, ensure_ascii=False, indent=4)
                f.close()

            message = bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                  text='⚠️Уведомление остановлено⚠️\n'
                                       'Укажите интервал чтоб запустить уведомление.'
                                  , reply_markup=keyboard_statistic(group_id, val),
                                  parse_mode="Markdown", disable_web_page_preview=True)

    if flag == 's4':
        group_id = data
        message = bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                        text='Напишите интервал автоматического отправления статистики. \n'
                                             'Указать время в МИНУТАХ',
                                        parse_mode="Markdown", disable_web_page_preview=True)
        bot.register_next_step_handler(message, stat_push, call, group_id)