# Тима Минский tg: https://t.me/tima_minski
# здесь формируется список бан-слов и выражений, записывает готовые результаты по списку в json файл группы.

from loader import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
from config import dt, fs


# клавиатура для списка бан-слов
def keyboard_ban_text(group_id,user_id,val):
    keyboard = InlineKeyboardMarkup(row_width=2)
    exitbutton = InlineKeyboardButton(text="выход ✖️", callback_data="ss")
    button2 = InlineKeyboardButton('Редактировать', callback_data='rv' + str(group_id))
    backbutton = InlineKeyboardButton('назад', callback_data="st:" + str(group_id))
    if val == '1':
        keyboard.add(button2,backbutton, exitbutton)
    elif val == '2':
        keyboard.add(backbutton, exitbutton)
    elif val == '3':
        keyboard.add(button2,backbutton, exitbutton)
    return keyboard


# функция принимает кнопку "Добавить бан слова"
def text_ban(call,group_id):
    user_id = call.message.chat.id
    val = '1'
    with open(f'groups/{str(group_id)}/list_banned_words.json', "r", encoding="utf-8") as f:
        list_words = json.loads(f.read())
        f.close()
        # список бан слов пустой
        if len(list_words['banned_message']) == 0:
            bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                  text=f'Ваш список "ban" слов \n'
                                       f'на данный момент - пустой: 😔'
                                       f' \n'
                                       f' {list_words["banned_message"]} \n'
                                       f'Нажмите "Редактировать" чтоб добавить "ban" слова 👌',
                                  reply_markup=keyboard_ban_text(group_id, user_id, val), parse_mode='Markdown',
                                  disable_web_page_preview=True)
        # список бан слов не пустой
        if len(list_words['banned_message']) > 0:
            bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                  text=f'Вот список "ban" слов 😊\n\n'
                                       f' {list_words["banned_message"]} \n\n'
                                       f'Нажмите "Редактировать", если хотите изменить список 👍 ',
                                  reply_markup=keyboard_ban_text(group_id, user_id, val), parse_mode='Markdown',
                                  disable_web_page_preview=True)


# загружает данные json файла со списком бан-слов
def change_ban_words(group_id):
    with open(f'groups/{str(group_id)}/list_banned_words.json', "r", encoding="utf-8") as f:
        list_words = json.loads(f.read())
        f.close()
    buf = []
    try:
        for x in list_words['banned_message']:
            buf.append(x)
    except:
        pass
    return buf


# редактирует файл с бан словами, добавляет или удаляет и сохраняет в json
def message_write(message,call,group_id):
    with open(f'groups/{str(group_id)}/list_banned_words.json', "r", encoding="utf-8") as f:
        list_words = json.loads(f.read())
        f.close()
    buf = []
    try:
        for x in list_words['banned_message']:
            buf.append(x)
    except:
        pass

    val ='3'
    user_id = call.message.chat.id

    # принимает сообщение и добавляет его в бан лист, если в сообщении нет слова del/
    if message.content_type == "text" and message.text.replace(" ", "") != "" and 'del/' not in message.text:
        message.text = message.text.split(',')
        for x in message.text:
            buf.append(x)
        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text=f'Cохранено ☺️\n'
                                   f'Вот список "ban" слов 😊\n\n'
                                   f' {buf} \n\n'
                                   f'Нажмите "Редактировать", чтоб изменить список 👌\n',
                              reply_markup=keyboard_ban_text(group_id, user_id, val),
                              parse_mode="Markdown", disable_web_page_preview=True)


    # принимает сообщение и удаляет его из бан-листа, если в сообщении есть слова del/
    if message.content_type == "text" and 'del/' in message.text:

        # удаляет пробелы в сообщении и бан-листе, сверяет и выдает бан-лист с удаленными словами/фразами
        message.text = message.text.replace("del/", "").replace(" ", "")
        message.text = message.text.split(',')

        for x in buf:
            if x.replace(" ", "") in message.text:
                buf.remove(x)

        bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text=f'Cохранено ☺️\n'
                                   f'Вот список "ban" слов 😊\n\n'
                                   f' {buf} \n\n'
                                   f'Нажмите "Редактировать", чтоб изменить список 👌\n',
                              reply_markup=keyboard_ban_text(group_id, user_id, val),
                              parse_mode="Markdown", disable_web_page_preview=True)
    list_words['banned_message'] = buf
    with open(f'groups/{str(group_id)}/list_banned_words.json', "w", encoding="utf-8") as f:
        json.dump(list_words, f, ensure_ascii=False, indent=4)
    f.close()
    bot.delete_message(message.chat.id, message.message_id)


def handler_ban_words(call):
    idx = call.message.chat.id
    user_id = call.message.chat.id
    data = dt(call.data)
    flag = fs(call.data)
    # флаг кнопки "Редактировать", добавляет или удаляет бан слова
    if flag == 'rv':
        val = '2'
        group_id = data
        buf = change_ban_words(group_id)
        message = bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                              text=f'Вот список "ban" слов 😊\n\n'
                                       f' {buf} \n\n'
                                       f'Чтоб добавить "ban" слова, напишите их\nчерез "," одним сообщением 👌\n\n'
                                       f'Чтобы удалить "ban" слова, напишите \n"del/" и слова через "," одним сообщением. 👍 ',
                              reply_markup=keyboard_ban_text(group_id, user_id, val),
                              parse_mode="Markdown", disable_web_page_preview=True)

        bot.register_next_step_handler(message,message_write,call,group_id)




