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
    button4 = InlineKeyboardButton("Опубликовать", callback_data="pr" + str(group_id))

    exitbutton = InlineKeyboardButton(text="выход ✖️", callback_data="ss")
    backbutton = InlineKeyboardButton('назад', callback_data="st:" + str(group_id))
    backbutton2 = InlineKeyboardButton('назад', callback_data="du" + str(group_id))
    time1 = InlineKeyboardButton('30 мин', callback_data="ti30" + str(group_id))
    time2 = InlineKeyboardButton('60 мин', callback_data="ti60" + str(group_id))
    time3 = InlineKeyboardButton('Задать свое', callback_data="ti00" + str(group_id))


    if val =="0":
        keyboard.add(button1, button2, backbutton, exitbutton)
    if val == "1":
        keyboard.add(backbutton2, exitbutton)
    if val == "2":
        keyboard.add(button3, button4,backbutton2,exitbutton)
    if val == "3":
        keyboard.add(time1,time2,time3,backbutton2)

    return keyboard



def notification(call, group_id):
    val = "0"
    with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
        list = json.load(f)
        f.close()
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text='Меню уведомлений 🔔',
                              reply_markup=keyboard(call,group_id,val), parse_mode='Markdown',
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


        with open(f'groups/{str(group_id)}/push_notifications.json', "w", encoding="utf-8") as f:
            json.dump(list, f, ensure_ascii=False, indent=4)
            f.close()
        bot.delete_message(message.chat.id, message.message_id)


# функция редактирует новое уведомление
def create_notification(message, call, group_id):
    val = "2"
    with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
        list = json.loads(f.read())
        f.close()


    if message.content_type == "text" and message.text.replace(" ", "") != "":
        list["new"] = (message.text)
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text='Выглядит уведомление вот так: 😊\n\n' + list["new"]
                              , reply_markup=keyboard(call, group_id, val),
                              parse_mode="Markdown", disable_web_page_preview=True)
        with open(f'groups/{str(group_id)}/push_notifications.json', "w", encoding="utf-8") as f:
            json.dump(list, f, ensure_ascii=False, indent=4)
            f.close()
    bot.delete_message(message.chat.id, message.message_id)

def time_notifications(time_,group_id):
    while True:

        with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
            list = json.loads(f.read())
            f.close()

        bot.send_message(group_id, text=list['new'])
        time.sleep(time_)




# функция публикует уведомление
def public_notifications(call, group_id):
    val ="3"
    with open(f'groups/{str(group_id)}/push_notifications.json', "r", encoding="utf-8") as f:
        list = json.load(f)
        f.close()
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text='Выглядит уведомление вот так: 😊\n\n' + list["new"] +
                              '\n\n Укажите интервал оповещения.'
                              , reply_markup=keyboard(call, group_id, val),
                              parse_mode="Markdown", disable_web_page_preview=True)

def handler_notifications(call):
    data = dt(call.data)
    flag = fs(call.data)
# создать новое уведомление
    if flag == "cn":
        val = "1"
        group_id = data
        message = bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text='Напиши новое уведомление 🔔\n'
                                   'одним сообщением',
                              reply_markup=keyboard(call, group_id, val), parse_mode='Markdown',
                              disable_web_page_preview=True)

        bot.register_next_step_handler(message, new_notification, call, group_id)


    if flag == "an":
        print("hi")


 # редактировать уведомление
    if flag=="cr":
        val = "2"
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

# опубликовать уведомление
    if flag == "pr":
        group_id = data
        public_notifications(call, group_id)


    if flag == "ti":
        data_time = int(data[:2])*60
        group_id = int(data[2:])

        t = threading.Thread(target=time_notifications, args=(5,group_id))  # 100 время на которое функция засыпает
        t.start()




