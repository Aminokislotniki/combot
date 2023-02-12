import json
import os
import sys


def karma(message):
    group_id = message.chat.id  # id группы
    message_user = message.from_user.id
    print(message_user)

    with open(f'groups/{str(group_id)}/{str(group_id)}.json', "r", encoding="utf-8") as f:
        list = json.loads(f.read())

        f.close()

    with open(f'groups/{str(group_id)}/chat_history.json', "r", encoding="utf-8") as r:
        chat_history = json.loads(r.read())
        r.close()

        # добавляем сообщение в количество сообщений у пользователя
        list_message = []
        for x in chat_history["chat_text"]:
            if x['user'] == message_user:
                list_message.append(x)
        for y in list['subscribers']:
            if y['id_user'] == message_user:
                y['karma']['all_messages'] = len(list_message)
        with open(f'groups/{str(group_id)}/{str(group_id)}.json', "w", encoding="utf-8") as f:
            json.dump(list, f, ensure_ascii=False, indent=4)
            f.close()

