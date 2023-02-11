from loader import bot, id_bot
import json
import os
from admin_functionality.add_group import check_is_group,group_file_archive


# функция проверяет наличие нового пользователя по ID в json файле группы
# если пользователя в списке нет, то добавляет
def check_is_user(message, group_id,new_user_id):
    list_admin_group = bot.get_chat_administrators(chat_id=group_id)  # все админы чата, включая владельца
    number_of_subscribers = bot.get_chat_member_count(chat_id=group_id)  # колличество подписчиков чата
    with open(f'groups/{str(group_id)}/{str(group_id)}.json', "r", encoding="utf-8") as f:
        list_group = json.loads(f.read())
        f.close()

    # добавление администраторов и владельца в json groups
    for admin in list_admin_group:
        admin_id = admin.user.id
        admin_name = admin.user.first_name
        admin_username = admin.user.username
        admin_status = admin.status #creator
        buf_list = []
        if admin_status == "creator":
            list_group['creator'] = admin_id
        if admin_status == 'administrator':
            for x in list_group['admin_group']:
                buf_list.append(x['id_user'])
            if admin_id not in buf_list:
                list_group['admin_group'].append({'id_user': admin_id,
                                                  'user_name': admin_name})

    # добавление нового пользователя в json groups
    new_user_id = message.new_chat_members[0].id
    new_user_first_name = message.new_chat_members[0].first_name
    new_user_username = message.new_chat_members[0].username
    new_user_is_bot = message.new_chat_members[0].is_bot

    for i in range(len(list_group['subscribers_del'])):
        if str(new_user_id) in str(list_group['subscribers_del'][i]['id_user']):
            del list_group['subscribers_del'][i]
            break

    buf_list_new_user = []
    for x in list_group['subscribers']:
        buf_list_new_user.append(x['id_user'])
    if new_user_id not in buf_list_new_user:
        list_group['subscribers'].append({'id_user': new_user_id,
                                        'user_name': new_user_first_name,
                                        'user_username': new_user_username,
                                        'status': "active",
                                        'photo': "null",
                                        'description': "null"})

    list_group['number_of_subscribers'] = number_of_subscribers
    list_group["subscribers_del_number"] = len(list_group['subscribers_del'])  # колличество удаленных пользователей
    with open(f'groups/{str(group_id)}/{str(group_id)}.json', "w", encoding="utf-8") as f:
        json.dump(list_group, f, ensure_ascii=False, indent=4)


# Функция проверяет наличие файла админа по ID в json файле администраторов
# если файла нет, то добавляет. В файл записывает: владельца -> какие группы держит
def check_is_admin(message, group_id):
    list_admin_group = bot.get_chat_administrators(chat_id=group_id)
    group_title = message.chat.title
    for admin in list_admin_group:
        admin_id = admin.user.id
        admin_name = admin.user.first_name
        admin_username = admin.user.username
        admin_status = admin.status #creator
        if admin_status == "creator":
            try:
                with open("administrator/" + str(admin_id) + ".json", "r", encoding="utf-8") as f:
                    buf = json.loads(f.read())
                    f.close()
                    group_list = buf['group']
                    buf_list = []
                    for x in group_list:
                        if x['group_id'] not in buf_list:
                            buf_list.append(x['group_id'])
                    if group_id not in buf_list:
                        group_list.append({'group_id': group_id, 'group_name': group_title})

                    with open("administrator/" + str(admin_id) + ".json", "w", encoding="utf-8") as f:
                        json.dump(buf, f, ensure_ascii=False, indent=4)
            except:
                admin_dict = dict({
                    "creator": admin_id,
                    "creator_name": admin_name,
                    "creator_username": admin_username,
                    "group": [{'group_id':group_id, 'group_name': group_title}]
                })
                with open("administrator/" + str(admin_id) + ".json", "w", encoding="utf-8") as f:
                    json.dump(admin_dict, f, ensure_ascii=False, indent=4)


# функция ловит удаленных пользователей, записывает в файл
def check_del_user(message,group_id):
    creator_id = message.from_user.id
    del_user_id = message.left_chat_member.id
    del_user_name = message.left_chat_member.first_name
    user_username = message.left_chat_member.username
    number_of_subscribers = bot.get_chat_member_count(chat_id=group_id)  # колличество подписчиков чата
    with open(f'groups/{str(group_id)}/{str(group_id)}.json', "r", encoding="utf-8") as f:
        list_group = json.loads(f.read())

    # удаляем пользователя из списка активных подписчиков
    for i in range(len(list_group['subscribers'])):
        if str(del_user_id) in str(list_group['subscribers'][i]['id_user']):
            del list_group['subscribers'][i]
            break

    # если пользователь был администратором, то удаляем его из списка администраторов
    for i in range(len(list_group['admin_group'])):
        if str(del_user_id) in str(list_group['admin_group'][i]['id_user']):
            del list_group['admin_group'][i]
            break


    # добавляем удаленного пользователя в файле группы в список "subscribers_del"
    buf_list_new_user = []
    for x in list_group['subscribers_del']:
        buf_list_new_user.append(x['id_user'])
    if del_user_id not in buf_list_new_user:
        list_group['subscribers_del'].append({'id_user': del_user_id,
                                          'user_name': del_user_name,
                                          'user_username': user_username,
                                          'status': "delete",
                                          'photo': "null",
                                          'description': "null"
                                              })

        list_group["subscribers_del_number"] = len(list_group['subscribers_del']) # колличество удаленных пользователей
        list_group["number_of_subscribers"] = number_of_subscribers # колличество подписчиков чата
    with open(f'groups/{str(group_id)}/{str(group_id)}.json', "w", encoding="utf-8") as f:
        json.dump(list_group, f, ensure_ascii=False, indent=4)


# обрабатывает всех, кто подписался/добавили в группу
def new_memders(message):
    print("hello")
    group_title = message.chat.title # название группы
    group_id = message.chat.id # id группы
    new_user_id = message.new_chat_members[0].id
    new_user_name = message.new_chat_members[0].last_name
    if new_user_id == int(id_bot):
        check_is_group(group_id,group_title)  # добавляет файл группы
    else:
        bot.send_message(message.chat.id, "Добро пожаловать, {0}!".format(new_user_name))

        check_is_user(message, group_id,new_user_id)

    check_is_admin(message, group_id)  # добавляет владельца


# обрабатывает всех, кто удалился из группы
def left_member(message):
    group_id = message.chat.id  # id группы
    print("User " + message.left_chat_member.first_name + " left")
    try:
        if message.left_chat_member.id != int(id_bot):
            check_del_user(message, group_id)
        if message.left_chat_member.id == int(id_bot):
            print("про")
            group_file_archive(message, group_id)
    except OSError:
        pass