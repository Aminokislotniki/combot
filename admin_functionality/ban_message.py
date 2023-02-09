from loader import bot
import json
import re



# функция принимает все сообщения и сортирует по группам
def message_sharing(message):
    group_id = message.chat.id
    message_text = message.text
    message_time = message.date
    message_user = message.from_user.id
    save_text = {"date": message_time, "user": message_user, "text": message_text}
    try:
        with open(f'groups/{str(group_id)}/chat_history.json', "r", encoding="utf-8") as f:
            buf = json.loads(f.read())
            buf["chat_text"].append(save_text)
            number_message = len(buf["chat_text"])
            buf["number_message"] = number_message
            f.close()
        with open(f'groups/{str(group_id)}/chat_history.json', "w", encoding="utf-8") as f:
            json.dump(buf, f, ensure_ascii=False, indent=4, )
            f.close()
    except:
        text = {"number_message":[1],
                "chat_text":[save_text]}
        with open(f'groups/{str(group_id)}/chat_history.json', "a", encoding="utf-8") as f:
            json.dump(text, f, ensure_ascii=False, indent=4, )
            f.close()


#получаем текст сообщения и удаляяем все пробелы таким образом вычисляем бан слова
def clean_chat(message):
    group_id = message.chat.id
    # получаем текст сообщения и удаляяем все пробелы
    text = message.text.lower().replace(' ', '')
    text_moder = "".join(c for c in text if c.isalnum())
    f = open('groups/' + str(group_id) + '/list_banned_words.json', 'r', encoding='utf-8')
    data = json.load(f)
    for x in data['banned_message']:
        if x in text_moder:
            bot.delete_message(message.chat.id, message.message_id)


# хэндлер работает только в супергруппах chat_types=['group'], в боте не фурычит
@bot.message_handler(chat_types=['supergroup'], content_types=["text"])
def check_banned_message(message):
    message_sharing(message)
    clean_chat(message)


# хэндлер работает только в группах chat_types=['group'], в боте не фурычит
@bot.message_handler(chat_types=['group'], content_types=["text"])
def check_banned_message(message):
    message_sharing(message)
    clean_chat(message)


