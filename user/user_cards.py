import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot


def info_change_photo_discription(message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton("Фото", callback_data="p1" + str(message.chat.id))
    button2 = InlineKeyboardButton("Описание", callback_data="p2"+ str(message.chat.id))
    keyboard.add(button1, button2)
    return keyboard
def user_card(message):
    group_id = message.chat.id
    if message.text == "/info":
        g = open('groups/' + str(group_id) + '/' + str(group_id) + '.json', 'r', encoding='utf-8')
        user_list = json.load(g)

        if message.reply_to_message != None:
            name = message.reply_to_message.from_user.first_name
            username = message.reply_to_message.from_user.username
            user_id = message.reply_to_message.from_user.id
            print("jhgkjhfg" + str(user_id))
            for x in user_list["subscribers"]:
                if x["id_user"] == int(user_id):
                    print(x)
                    bot.send_message(message.chat.id, f'📊<b>Статистика</b> {name}\n'
                                                      f'🏆<b>Репутация:</b> {x["karma"]["reputation"]}\n'
                                                      f'👤<b>ID:</b> {user_id}\n'
                                                      f'🚫<b>Нарушения:</b> {x["karma"]["ban_words"]} \n\n'
                                                      f'Можно добавить \n'
                                                      f'📝<b>Описание:</b> /info_change\n'
                                                      f'📷<b>Фото:</b> /info_change', parse_mode="html")

        else:

            name = message.from_user.first_name
            username = message.from_user.username
            user_id = message.from_user.id
            for i in user_list["subscribers"]:
                if i["id_user"] == int(user_id):
                    bot.send_message(message.chat.id, f'📊<b>Статистика</b> {name}\n'
                                              f'🏆<b>Репутация:</b> {i["karma"]["reputation"]}\n'
                                              f'👤<b>ID:</b> {user_id}\n'
                                              f'🚫<b>Нарушения:</b> {i["karma"]["ban_words"]} \n\n'
                                              f'Можно добавить \n'
                                              f'📝<b>Описание:</b> /info_change\n'
                                              f'📷<b>Фото:</b> /info_change', parse_mode="html")
        g.close()
    if message.text == "/commands":
        bot.send_message(message.chat.id, f'Команды группы: \n'
                                          f'📊 /info - просмотреть информацию о пользователе.\n'
                                          f'📷 /info_change - изменить картинку или описание')

    if message.text == "/info_change":
        bot.send_message(message.from_user.id, f"Привет {message.from_user.first_name}, выбери что хочешь добавить!"
                                                , reply_markup=info_change_photo_discription(message))
        bot.delete_message(message.chat.id, message.message_id)
