# Тима Минский tg: https://t.me/tima_minski
# Сортировка сообщений по файлам группы, контроль бан слов

from loader import bot
import json



# Функция принимает все сообщения и сортирует по группам, за каждым пользователем
# Когда пользователь пишет сообщение - файл с данными пользователя обновляется
def message_sharing(message):
    group_id = message.chat.id  # id группы
    list_admin_group = bot.get_chat_administrators(chat_id=group_id)  # все админы чата, включая владельца
    number_of_subscribers = bot.get_chat_member_count(chat_id=group_id)  # колличество подписчиков чата
    message_text = message.text
    message_time = message.date
    message_user = message.from_user.id
    save_text = {"date": message_time, "user": message_user, "text": message_text}
    # добавляет новое сообщение
    with open(f'groups/{str(group_id)}/chat_history.json', "r", encoding="utf-8") as f:
        buf = json.loads(f.read())
        buf["chat_text"].append(save_text)
        number_message = len(buf["chat_text"])
        buf["number_message"] = number_message
        f.close()
    with open(f'groups/{str(group_id)}/chat_history.json', "w", encoding="utf-8") as f:
        json.dump(buf, f, ensure_ascii=False, indent=4, )
        f.close()

    # ловит сообщение и добавляет пользователя в файл подписчиков группы.
    user_first_name = message.from_user.first_name
    user_username = message.from_user.username
    with open(f'groups/{str(group_id)}/{str(group_id)}.json', "r", encoding="utf-8") as f:
        list_group = json.loads(f.read())
        buf_list_new_user = []
        for x in list_group['subscribers']:
            buf_list_new_user.append(x['id_user'])
        if message_user not in buf_list_new_user:
            list_group['subscribers'].append({'id_user': message_user,
                                              'user_name': user_first_name,
                                              'user_username': user_username,
                                              'status': "active",
                                              'photo': "",
                                              'description': "",
                                              'karma': {
                                                        'ban_words': 0,
                                                        'bad_comment': 0,
                                                        'good_comment': 0,
                                                        'all_messages': 0,
                                                        "reputation": 0}
                                              })

        list_group['number_of_subscribers'] = number_of_subscribers
        list_group["subscribers_del_number"] = len(list_group['subscribers_del'])  # колличество удаленных пользователей
        with open(f'groups/{str(group_id)}/{str(group_id)}.json', "w", encoding="utf-8") as f:
            json.dump(list_group, f, ensure_ascii=False, indent=4)
            f.close()


#получаем текст сообщения и удаляяем все пробелы таким образом вычисляем бан слова
def clean_chat(message):
    group_id = message.chat.id
    # получаем текст сообщения и удаляяем все пробелы
    text = message.text.lower().replace(' ', '')
    text_moder = "".join(c for c in text if c.isalnum())
    f = open('groups/' + str(group_id) + '/list_banned_words.json', 'r', encoding='utf-8')
    data = json.load(f)
    g = open('groups/' + str(group_id) + '/' + str(group_id) + '.json', 'r', encoding='utf-8')
    user_list = json.load(g)
    g.close()
    buf = []
    for x in data['banned_message']:
        if x in text_moder:
            for i in user_list["subscribers"]:
                if i["id_user"] == message.from_user.id:
                    i["karma"]["ban_words"] = i["karma"]["ban_words"]+1
                    buf = i["karma"]["ban_words"]
                    with open('groups/' + str(group_id) + '/' + str(group_id) + '.json', "w", encoding="utf-8") as f:
                        json.dump(user_list, f, ensure_ascii=False, indent=4)

                        bot.reply_to(message, text=f'🔎 Замечено "плохое слово"!\n'
                                                       f'🙎 Его написал <b>"{message.from_user.first_name}"</b>\n'
                                                       f'😡 Не надо такое писать. Предупреждение № {buf}', parse_mode="html")
                        bot.delete_message(message.chat.id, message.message_id)




