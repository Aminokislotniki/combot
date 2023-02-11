from bot_functionality.statistics_group import statistic_group
from loader import bot
from config import dt, fs
import json
from keyboards import statistics_keyboard, return_keyboard, group_menu_stat
from config import loser_text
from bot_functionality.ban_words import text_ban
from admin_functionality.push_notifications import notification


# функция хэндлер "статистика" принимает call
def handler_statistic(call):
    idx = call.message.chat.id
    user_id = call.message.chat.id
    data = dt(call.data)
    flag = fs(call.data)

    # флаг для выброса статистики по активным группам владельца из файла "id.json"
    # директория "administrator"
    if flag == 'st':
        num = 'statist'
        if data[0] == "*":
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
                                          text="👥 <b>Выберете группу.</b>\nстраница - " + str(page + 1),
                                          reply_markup=statistics_keyboard(statistic, page, user_id), parse_mode='html')
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
            group_id = (data[1:])
            print(group_id)
            bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                  text='Меню группы, выбирай что хочешь сделать! ',
                                  reply_markup=group_menu_stat(group_id,user_id), parse_mode='Markdown',
                                  disable_web_page_preview=True)

    # флаг добавляет регулярного сообщения (раз в n времени присылается ботом)
    if flag == "du":
        group_id = data
        notification(call, group_id)
    # флаг выдает список бан слов, и две кнопки, редактировать и сохранить
    if flag == "bv":
        group_id = data
        text_ban(call,group_id)
    # флаг выдает статистику по группе (сколько подписчиков, сообщений, и прочее)
    if flag == "su":
        group_id = data
        statistic_group(call,group_id)
    # флаг выдает редактор профиля
    if flag == "rp":
        pass