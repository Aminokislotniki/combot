# Тима Минский tg: https://t.me/tima_minski
# поощрения и наказания
from loader import bot
import json

group_id = -839915842

def karma(message):
    group_id = message.chat.id
    message_text = message.text
    message_time = message.date
    message_user = message.from_user.id
    with open(f'groups/{str(group_id)}/chat_history.json', "r", encoding="utf-8") as f:
        chat_history = json.loads(f.read())
    f.close()


with open('groups/'+str(group_id)+'/chat_history.json', "r", encoding="utf-8") as f:
    chat_history = json.load(f)
    print(chat_history)
    f.close()