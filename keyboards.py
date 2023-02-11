# Тима Минский tg: https://t.me/tima_minski
# все клавиатуры проекта

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json


#Стартовая клавиатура, флаг st,in
def start_keyboard(user_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_1 = InlineKeyboardButton('➕Добавить в чат ', url='https://t.me/manager_chat_tim_bot?startgroup')
    button_2 = InlineKeyboardButton('Статистика 📈', callback_data='st*0'+str(user_id))
    button_3 = InlineKeyboardButton('Инфо 📄', callback_data='in')
    keyboard.add(button_1,button_2,button_3)
    return keyboard


# клавиатура для отображения групп, где бот является админом, флаг st,ss
def statistics_keyboard(statistic,page_number,user_id):
    print(f' номер страницы {page_number}')
    keyboard = InlineKeyboardMarkup(row_width=2)
    backbutton = InlineKeyboardButton(text="🔙 предыдущие ", callback_data="st*" + str(page_number - 1)+str(user_id))
    nextbutton = InlineKeyboardButton(text="следующие 🔜", callback_data="st*" + str(page_number + 1)+str(user_id))
    exitbutton = InlineKeyboardButton(text="выход ✖️", callback_data="ss")
    if len(statistic) < 6:
        button_list = [InlineKeyboardButton(text=x["group_name"], callback_data="st:" + str(x['group_id']))
                       for x in statistic]
        keyboard.add(*button_list)
    elif 6*(page_number + 1) < len(statistic) and 6 * page_number <= 0:
        button_list = [InlineKeyboardButton(text=x["group_name"], callback_data="st:" + str(x['group_id'])) for x in
                       statistic[page_number * 6:(page_number + 1) * 6]]
        keyboard.add(*button_list)
        keyboard.add(nextbutton)
    elif 5*(page_number+1) >= len(statistic):
        button_list = [InlineKeyboardButton(text=x["group_name"], callback_data="st:" + str(x['group_id'])) for x in
                       statistic[page_number * 6:(page_number + 1) * 6]]
        keyboard.add(*button_list)
        keyboard.add(backbutton)
    else :
        button_list = [InlineKeyboardButton(text=x["group_name"], callback_data="st:" + str(x['group_id'])) for x in
                       statistic[page_number * 6:(page_number + 1) * 6]]
        keyboard.add(*button_list)
        keyboard.add(backbutton, nextbutton)
    keyboard.add(exitbutton)
    return keyboard


# клавиатура информативная, для возврата в меню и инфо, флаг in,ss
def return_keyboard(num):
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_1 = InlineKeyboardButton('➕ Все понятно', callback_data='ss')
    button_2 = InlineKeyboardButton('Инфо 📄', callback_data='in')
    if num == "info":
        keyboard.add(button_1,)
    elif num == "statist":
        keyboard.add(button_1, button_2)
    return keyboard


# клавиатура отображает меню статистики для администратора по выбранной группе флаг du,bv,su,rp,st
def group_menu_stat(group_id,user_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton('Добавить уведомление', callback_data="du" + str(group_id))
    button2 = InlineKeyboardButton('Добавить BAN слова', callback_data="bv" + str(group_id))
    button3 = InlineKeyboardButton('Статистика', callback_data="su" + str(group_id))
    button4 = InlineKeyboardButton('Редактор профиля', callback_data="rp" + str(group_id))
    exitbutton = InlineKeyboardButton(text="выход ✖️", callback_data="ss")
    backbutton = InlineKeyboardButton(text="назад ✖️", callback_data='st*0'+str(user_id))
    keyboard.add(button1,button2,button3,button4,exitbutton,backbutton)
    return keyboard







