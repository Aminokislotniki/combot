# Тима Минский tg: https://t.me/tima_minski
# главные переменные, используются во всем проекте


import telebot

TOKEN_BOT = '6102379005:AAGFDiLzOSiB5lIXsQPyxOgTCa0eie7Ue5A'
id_bot = '6102379005'
name_bot = 'БотManager'
bot = telebot.TeleBot(TOKEN_BOT)
url_bot = '@manager_chat_tim_bot'


text_start = f'БотManager — самый популярный бот в Telegram \nдля управления группами. \n' \
             f'Аналитика, модерация, система репутации, \nтриггеры, отчеты и многое другое.\n\n' \
             f'Добавьте [БотManager](https://t.me/manager_chat_tim_bot?startgroup=hbase) в группу, ' \
             f'\nили назначьте его администратором.'

loser_text = f' К сожалению [БотManager](https://t.me/manager_chat_tim_bot?startgroup=hbase)' \
             f' не назначен администратором ни в какой Вашей группе... 😔 \n' \
             f' Вы можете сперва назначить его, и после смотреть "статистику" 😉'


info_text = f'Информация о функционале бота: {name_bot} \n\n'


