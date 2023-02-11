# Тима Минский tg: https://t.me/tima_minski
# здесь формируется текст пуш уведомления и настройка по времени
from loader import bot
from config import dt, fs
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import threading


# клавиатура для уведомлений
def keyboard(call,group_id,val):
    keyboard = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton("Создать новое", callback_data="cn"+str(group_id))
    button2 = InlineKeyboardButton("Все уведомления", callback_data="an"+str(group_id))
    button3 = InlineKeyboardButton("Редактировать", callback_data="cr"+str(group_id))
    button4 = InlineKeyboardButton("Добавить интервал", callback_data="pr" + str(group_id))


    exitbutton = InlineKeyboardButton(text="выход ✖️", callback_data="ss" + str(group_id))
    backbutton = InlineKeyboardButton('назад', callback_data="st:" + str(group_id))
    backbutton2 = InlineKeyboardButton('назад', callback_data="du" + str(group_id))
    backbutton3 = InlineKeyboardButton('назад', callback_data="pr" + str(group_id)) # интервал изменить
    backbutton4 = InlineKeyboardButton('назад', callback_data="cr" + str(group_id))  # текст изменить
    run_button = InlineKeyboardButton('Cтарт', callback_data="go++" + str(group_id))
    stop_button = InlineKeyboardButton('Cтоп', callback_data="go--" + str(group_id))
    del_button = InlineKeyboardButton('Удалить', callback_data="godl" + str(group_id))
    time1 = InlineKeyboardButton('30 мин', callback_data="ti30" + str(group_id))
    time2 = InlineKeyboardButton('60 мин', callback_data="ti60" + str(group_id))
    time3 = InlineKeyboardButton('Задать свое', callback_data="ti00" + str(group_id))


    if val =="0":
        keyboard.add(button1, backbutton, exitbutton)
    if val == "1":
        keyboard.add(backbutton2, exitbutton)
    if val == "2":
        keyboard.add(button3, button4,backbutton2,exitbutton)
    if val == "3":
        keyboard.add(time1,time2,time3,backbutton4,exitbutton)
    if val == "4":
        keyboard.add(stop_button,del_button,backbutton,exitbutton)
    if val == "5":
        keyboard.add(run_button,backbutton3,exitbutton)
    if val == "7":
        keyboard.add(run_button,del_button,backbutton,exitbutton)
    if val == "8":
        keyboard.add(stop_button,del_button,backbutton,exitbutton)
    if val == "9":
        keyboard.add(run_button,del_button,backbutton,exitbutton)



    return keyboard



def notification(call, group_id):
    with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
        list = json.load(f)
        f.close()
        if len(list['active']) == 0:
            val = "0"
            bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text='Меню уведомлений 🔔\n\n'
                                'У вас нет активного уведомления, но вы можете его добавить!',
                              reply_markup=keyboard(call,group_id,val), parse_mode='Markdown',
                              disable_web_page_preview=True)
        else:
            if list["public"] =="yes":
                val = "8"
                bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                      text='Меню уведомлений 🔔\n'
                                           '⚠️Уведомление запущено⚠️\n\n' + list['active'] +'\n\n У вас уже есть уведомление,'
                                           ' нажмите "Удалить" чтоб создать новое',
                                      reply_markup=keyboard(call, group_id, val), parse_mode='Markdown',
                                      disable_web_page_preview=True)
            if list["public"] == "no":
                val = "9"
                bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                      text='Меню уведомлений 🔔\n'
                                           '⚠️Уведомление остановлено⚠️\n\n' + list[
                                          'active'] + '\n\n У вас уже есть уведомление,'
                                                      ' нажмите "Удалить" чтоб создать новое',
                                      reply_markup=keyboard(call, group_id, val), parse_mode='Markdown',
                                      disable_web_page_preview=True)

# функция создает новое уведомление
def new_notification(message, call, group_id):
    val = "2"
    with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
        list = json.loads(f.read())
        f.close()

        if message.content_type == "text" and message.text.replace(" ", "") != "":
            list["new"] = (message.text)
            bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text= 'Выглядит уведомление вот так: 😊\n\n' + list["new"]
                                  ,reply_markup=keyboard(call,group_id,val),
                              parse_mode="Markdown", disable_web_page_preview=True)
        else:
            val = "0"
            bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                  text='⚠️ Ошибка при вводе текста ! еще раз внимательно введи '
                                       'ТЕКСТ ⚠️'
                                  , reply_markup=keyboard(call, group_id, val),
                                  parse_mode="Markdown", disable_web_page_preview=True)

        with open(f'groups/{str(group_id)}/push_notifications.json', "w", encoding="utf-8") as f:
            json.dump(list, f, ensure_ascii=False, indent=4)
            f.close()
        bot.delete_message(message.chat.id, message.message_id)


# функция редактирует новое уведомление текст
def create_notification(message, call, group_id):
    val = "2"
    with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
        list = json.loads(f.read())
        f.close()
    if message.content_type == "text" and message.text.replace(" ", "") != "":
        list["new"] = message.text
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text='Выглядит уведомление вот так: 😊\n\n' + list["new"]
                              , reply_markup=keyboard(call, group_id, val),
                              parse_mode="Markdown", disable_web_page_preview=True)
        with open(f'groups/{str(group_id)}/push_notifications.json', "w", encoding="utf-8") as f:
            json.dump(list, f, ensure_ascii=False, indent=4)
            f.close()
    else:
        val = "2"
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text='Выглядит уведомление вот так: 😊\n\n' + list["new"] +
                              '\n\n⚠️ Ошибка при вводе текста ! еще раз внимательно введи '
                                       'ТЕКСТ ⚠️'
                              , reply_markup=keyboard(call, group_id, val),
                              parse_mode="Markdown", disable_web_page_preview=True)
    bot.delete_message(message.chat.id, message.message_id)


#работает со временем уведомления
def time_notifications(call,group_id,data_time):
    val = "5"
    with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
        list = json.loads(f.read())
        f.close()
        list["new_time"] = data_time
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text='Выглядит уведомление вот так: 😊\n\n' + list["new"] +
                                   '\n\n Интервал оповещения каждые: ' + list["new_time"] + ' минут.'
                              , reply_markup=keyboard(call, group_id, val),
                              parse_mode="Markdown", disable_web_page_preview=True)
        with open(f'groups/{str(group_id)}/push_notifications.json', "w", encoding="utf-8") as f:
            json.dump(list, f, ensure_ascii=False, indent=4)
            f.close()


#работает со временем уведомления свой интервал
def time_notifications_user(message, call, group_id):

    with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
        list = json.loads(f.read())
        f.close()
        if message.content_type == ("text") and message.text.replace(" ", "") and message.text.isdigit():
            list["new_time"] = message.text
            val = "5"
            bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                  text='Выглядит уведомление вот так: 😊\n\n' + list["new"] +
                                       '\n\n Интервал оповещения каждые: ' + list["new_time"] + ' минут.'
                                  , reply_markup=keyboard(call, group_id, val),
                                  parse_mode="Markdown", disable_web_page_preview=True)
            with open(f'groups/{str(group_id)}/push_notifications.json', "w", encoding="utf-8") as f:
                json.dump(list, f, ensure_ascii=False, indent=4)
                f.close()

        else:
            val = "3"
            bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                  text='Выглядит уведомление вот так: 😊\n\n' + list["new"] +
                                       '\n\n ⚠️ Ошибка при вводе интервала! еще раз внимательно введи '
                                       'интервал в МИНУТАХ одним числом ⚠️'
                                  , reply_markup=keyboard(call, group_id, val),
                                  parse_mode="Markdown", disable_web_page_preview=True)
    bot.delete_message(message.chat.id, message.message_id)


# функция работает с текстом уведомления
def text_notifications(call, group_id):
    val ="3"
    with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
        list = json.load(f)
        f.close()
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text='Выглядит уведомление вот так: 😊\n\n' + list["new"] +
                              '\n\n Укажите интервал оповещения.'
                              , reply_markup=keyboard(call, group_id, val),
                              parse_mode="Markdown", disable_web_page_preview=True)

# функция запускает уведомление и останавливает
def start_notifications(control_notifications,call,time_,group_id):
    with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
        list = json.load(f)
        f.close()
    counter = 1
    while counter < 2:
        if thread_stop == True:
            print(counter)
            counter += 1
            time.sleep(0.5)

        bot.send_message(group_id, text=list['active'])
        time.sleep(time_)



def handler_notifications(call):
    data = dt(call.data)
    flag = fs(call.data)
# создать новое уведомление
    if flag == "cn":
        val = "1"
        group_id = data
        message = bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text='Напиши новое уведомление 🔔',
                              reply_markup=keyboard(call, group_id, val), parse_mode='Markdown',
                              disable_web_page_preview=True)

        bot.register_next_step_handler(message, new_notification, call, group_id)


    if flag == "an":
        group_id = data
        def all_notifications(group_id):
            with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
                list = json.load(f)
                f.close()
                if len(list['active']) > 0:
                    for x in list['active']:
                        message = bot.edit_message_text(message_id=call.message.message_id,
                                                        chat_id=call.message.chat.id,
                                                        text='Напиши новое уведомление 🔔',
                                                        reply_markup=keyboard(call, group_id, val),
                                                        parse_mode='Markdown',
                                                        disable_web_page_preview=True)

    # редактировать уведомление
    if flag=="cr":
        val = "1"
        group_id = data
        with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
            list = json.loads(f.read())
            f.close()
        message = bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text='Выглядит уведомление вот так: 😊\n\n' + list["new"] +
                                   '\n\n Можешь изменить текст'
                              , reply_markup=keyboard(call, group_id, val),
                              parse_mode="Markdown", disable_web_page_preview=True)

        bot.register_next_step_handler(message, create_notification, call, group_id)

    # работает с текстом уведомления
    if flag == "pr":
        group_id = data
        text_notifications(call, group_id)

    # работает со временем уведомления
    if flag == "ti":
        data_time = data[:2]
        group_id = data[2:]
        time_notifications(call, group_id, data_time)
        if data_time == "00":
            val ="2"
            with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
                list = json.loads(f.read())
                f.close()
            message = bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text='Выглядит уведомление вот так: 😊\n\n' + list["new"] +
                              '\n\nУкажите свой интервал времени в МИНУТАХ.'
                              , parse_mode="Markdown", disable_web_page_preview=True)

            bot.register_next_step_handler(message, time_notifications_user, call, group_id)

    # СТАРТ уведомления
    if flag == "go":
        print(data)
        control_notifications = data[:2]
        group_id = data[2:]

        global thread_stop
        if control_notifications =="++":
            val = "4"
            with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
                list = json.loads(f.read())
                f.close()
                list["active"] = list["new"]
                list["time"] = list["new_time"]
                list["public"] = "yes"

                bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                          text='Уведомление опубликовано 😊\n'
                                               'Выглядит уведомление вот так: \n\n' + list["active"] +
                                               '\n\n Интервал: ' + str(list["time"]) + ' минут.'
                                          , reply_markup=keyboard(call, group_id, val),
                                          parse_mode="Markdown", disable_web_page_preview=True)
                with open(f'groups/{str(group_id)}/push_notifications.json', "w", encoding="utf-8") as f:
                    json.dump(list, f, ensure_ascii=False, indent=4)
                    f.close()

                thread_stop = False
                thread = threading.Thread(target=start_notifications,args=(control_notifications,call,int(list["time"])*60,group_id))
                thread.start()


        if control_notifications == "--":
            thread_stop = True #Присваеваем значение True и завершаем поток
            val = "7"
            with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
                list = json.loads(f.read())
                f.close()
                list["public"] = "no"
            bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                  text='⚠️Уведомление остановлено⚠️ \n'
                                       'Выглядит уведомление вот так: 😊\n\n' + list["active"] +
                                       '\n\n Интервал: ' + str(list["time"]) + ' минут.'
                                  , reply_markup=keyboard(call, group_id, val),
                                  parse_mode="Markdown", disable_web_page_preview=True)
            with open(f'groups/{str(group_id)}/push_notifications.json', "w", encoding="utf-8") as f:
                json.dump(list, f, ensure_ascii=False, indent=4)
                f.close()


        if control_notifications == "dl":
            thread_stop = True  # Присваеваем значение True и завершаем поток

            with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
                list = json.loads(f.read())
                f.close()
                list["active"] = ""
                list["time"] = ""
                list["public"] = ""
            with open(f'groups/{str(group_id)}/push_notifications.json', "w", encoding="utf-8") as f:
                json.dump(list, f, ensure_ascii=False, indent=4)
                f.close()
                notification(call, group_id)






# def time_notifications(control_notifications,time_,group_id):
#     counter = 1
#     while counter < 2:
#         if thread_stop == True:
#             print(counter)
#             counter += 1
#             time.sleep(0.5)
#
#
#         with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
#             list = json.loads(f.read())
#             f.close()
#
#         bot.send_message(group_id, text=list['new'])
#         time.sleep(time_)
#
#         def mine_notifications(control_notifications,data_time,group_id):
#             global thread_stop
#             if control_notifications == "++":
#                 thread_stop = False
#                 thread = threading.Thread(target=time_notifications,args=(control_notifications,data_time,group_id))
#                 thread.start()
#             else:
#                 thread_stop = True  # Присваеваем значение True и завершаем поток
#
#         mine_notifications(control_notifications,data_time, group_id)