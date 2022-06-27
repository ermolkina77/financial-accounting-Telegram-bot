import gspread
import telebot


def balance(x):
    return x.get('B2')


def incomes(x):
    return x.get('B4')


def expenses(x):
    return x.get('B3')


def vvod(x, z, com):
    return x.append_row([z, com])


def perv(x, y):
    return x.update_cell(1, 2, y)


def delete(x, y):
    return x.delete_rows(y)


gs = gspread.service_account(filename='key.json')  # подключаем файл с ключами и пр.
sh = gs.open_by_key('116aygG_nIl3wwjS4FRh3OujUQFfdAM1DsAzjtyWSaMo')  # подключаем нужную нам таблицу по id
worksheet1 = sh.worksheet("доходы")
worksheet2 = sh.worksheet("расходы")
worksheet3 = sh.worksheet("выписка")
worksheet4 = sh.worksheet("долги")
new = 0
com = ' '
clas = ' '
rem = ' '
i = ' '
fir = ' '

bot = telebot.TeleBot('5471937213:AAEsJtJqtafxQ-O3WUG9al5RK9JjnD83wI4')  # подключаем бота


@bot.message_handler(content_types=['text'])  # метод получения сообщений
def get_text_messages(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id,
                         "/table дублирует ссылку на таблицу"
                         "\n/balance показывает текущий баланс"
                         "\n/incomes показывает сколько вы в общем заработали"
                         "\n/expenses показывает сколько вы в общем потратили"
                         "\n/first позволяет заполнить первоначальный баланс"
                         "\n/new добавляет запись"
                         "\n/delete удаляет запись"
                         "\n/end позволяет остановить текущую операцию")
    if message.text == "/new":
        bot.send_message(message.from_user.id, "Введите значение")
        bot.register_next_step_handler(message, get_new)
    if message.text == "/first":
        bot.send_message(message.from_user.id, "Введите первоначальный баланс")
        bot.register_next_step_handler(message, get_first)
    if message.text == "/delete":
        bot.send_message(message.from_user.id, "Напишите id записи (номер строки), которую хотите удалить")
        bot.register_next_step_handler(message, get_delete)
    if message.text == "/balance":
        bot.send_message(message.from_user.id, balance(worksheet3))
    if message.text == "/incomes":
        bot.send_message(message.from_user.id, incomes(worksheet3))
    if message.text == "/expenses":
        bot.send_message(message.from_user.id, expenses(worksheet3))
    if message.text == "/table":
        bot.send_message(message.from_user.id,
                         "Ссылка на таблицу https://docs.google.com/spreadsheets/d/116aygG_nIl3wwjS4FRh3OujUQFfdAM1DsAzjtyWSaMo/edit#gid=0")


def get_first(message):
    global fir
    if message.text == '/end':
        bot.send_message(message.from_user.id, "Операция остановлена")
    else:
        fir = int(message.text)
        perv(worksheet3, fir)
        bot.send_message(message.from_user.id, "Сделано")


def get_new(message):
    global new
    if message.text == '/end':
        bot.send_message(message.from_user.id, "Операция остановлена")
    else:
        new = int(message.text)
        bot.send_message(message.from_user.id, "Введите комментарий")
        bot.register_next_step_handler(message, get_com)


def get_com(message):
    global com
    if message.text == '/end':
        bot.send_message(message.from_user.id, "Операция остановлена")
    else:
        com = message.text
        bot.send_message(message.from_user.id, "Укажите вид записи (доход/расход/долг)")
        bot.register_next_step_handler(message, get_clas)


def get_clas(message):
    global clas
    if message.text == '/end':
        bot.send_message(message.from_user.id, "Операция остановлена")
    else:
        clas = message.text
        if clas == 'доход':
            vvod(worksheet1, new, com)
        elif clas == 'расход':
            vvod(worksheet2, new, com)
        elif clas == 'долг':
            vvod(worksheet4, new, com)
        bot.send_message(message.from_user.id, "Сделано")


def get_delete(message):
    global i
    if message.text == '/end':
        bot.send_message(message.from_user.id, "Операция остановлена")
    else:
        i = int(message.text)
        bot.send_message(message.from_user.id, "Укажите вид записи (доход/расход/долг)")
        bot.register_next_step_handler(message, get_clas1)


def get_clas1(message):
    global rem
    if message.text == '/end':
        bot.send_message(message.from_user.id, "Операция остановлена")
    else:
        rem = message.text
        if rem == 'доход':
            delete(worksheet1, i)
        elif rem == 'расход':
            delete(worksheet2, i)
        elif rem == 'долг':
            delete(worksheet4, i)
        bot.send_message(message.from_user.id, "Сделано")


bot.polling(none_stop=True, interval=0)
