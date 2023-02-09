from loader import bot, id_bot
import json
import os


# функция проверяет наличие файла с названием группы в директории "group" при подключении бота
# если файла нет, то добавляет, в файл записывает: id группы -> список администраторов, кто владелец,
# сколько подписчиков, и т.д
def check_is_group(group_id,group_title):
    try:
        with open(f'groups/{str(group_id)}/{str(group_id)}.json', "r", encoding="utf-8") as f:
            f.close()
            print(f'файл с ID группы "{group_id}" есть.')
        return True
    except:
        path = os.getcwd()
        os.makedirs(f'groups/{group_id}',exist_ok=True)
        with open(f'groups/{str(group_id)}/{str(group_id)}.json', "w", encoding="utf-8") as f:
            group_list = dict({'group_id': group_id,
                               'name_group': group_title,
                               'creator': 'null',
                               'admin_group': [],
                               'number_of_subscribers': 'null',
                               'subscribers': [],
                               'subscribers_ban_number': 'null',
                               'subscribers_ban': [],
                               'subscribers_del_number': 'null',
                               'subscribers_del': []
                               })
            json.dump(group_list, f, ensure_ascii=False, indent=4)
        print(f'добавил файл с ID новой группы: "{group_id}"')

        # добавляем файл бан слов(пустой файл)
        list_ban = {"banned_message": []}
        with open(f'groups/{str(group_id)}/list_banned_words.json', "w", encoding="utf-8") as f:
            json.dump(list_ban, f, ensure_ascii=False, indent=4)
        f.close()
        return False


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

    try:
        for x in range(len(list_group['subscribers_del'])):
            if list_group['subscribers_del'][x]['id_user'] == new_user_id:
                del list_group['subscribers_del'][x]
    except IndexError:
        pass

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


# функция перекидывает папку с данными группы в архив,
# если пользователь снова добавил бота в группу, то создается новая папка,
# таким образом сохраниться вся история добавления и удаления бота в группе
def group_file_archive(message,group_id):
    # Если удалили "БoтManager" из группы, весь архив остается, у админа в json группа удаляется
    # папка с данными группы (название папки - ID группы) перекидывается в архивную папку
    creator_id = message.from_user.id

    try:
        with open("administrator/" + str(creator_id) + ".json", "r", encoding="utf-8") as f:
            list = json.loads(f.read())
            for x in range(len(list['group'])):
                if list['group'][x]['group_id'] == int(group_id):
                    del list['group'][x]
        with open("administrator/" + str(creator_id) + ".json", "w", encoding="utf-8") as f:
            json.dump(list, f, ensure_ascii=False, indent=4)
        f.close()
        print(" админ удален")
    except IndexError:
        print(" админ не удален")
        pass


    num = 1
    x = 2
    while x > 1:
        try:
            os.replace(os.getcwd() + '/groups/' + str(group_id),
                       os.getcwd() + '/archive_group/' + str(group_id))
            break
        except PermissionError:
            num = num + 1
            try:
                text = f'({num})'
                os.rename(os.getcwd() + '/groups/' + str(group_id),
                          os.getcwd() + '/archive_group/' + str(group_id) + str(text))
                break
            except FileExistsError:
                x = 2
                pass


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
    try:
        for x in range(len(list_group['subscribers'])):
            if list_group['subscribers'][x]['id_user'] == del_user_id:
                del list_group['subscribers'][x]
    except IndexError:
        pass

    # если пользователь был администратором, то удаляем его из списка администраторов
    try:
        for x in range(len(list_group['admin_group'])):
            if list_group['admin_group'][x]['id_user'] == del_user_id:
                del list_group['admin_group'][x]
    except IndexError:
        pass

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
@bot.message_handler(content_types=["new_chat_members"])
def handler_new_member(message):
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
@bot.message_handler(content_types=['left_chat_member'])
def not_greeting(message):
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