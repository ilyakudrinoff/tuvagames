import os

import telebot
import sqlite3
import datetime
from telebot import types
from telegram.constants import ParseMode
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv('BOT_KEY'))  # - testingbot

user = None


@bot.message_handler(commands=['start'])
def start_message(message):
    global user
    user = message.from_user.id
    keyboard = types.InlineKeyboardMarkup()
    kb1 = types.InlineKeyboardButton(text="Давай попробуем", callback_data="text1")
    kb2 = types.InlineKeyboardButton(text="Не мое", callback_data="text2")
    keyboard.add(kb1, kb2)
    bot.send_message(message.chat.id, '*Привет!*\nМеня создали для того, чтобы люди из разных концов нашей страны '
                                      'почувствовали себя немного *счастливее*. Однажды каждый осознанный человек '
                                      'приходит к простому выводу: жить с позицией *\"отдавать\"* намного приятнее и '
                                      'правильнее, чем с позицией *\"брать\"*.\n\nМожет попробуем подарить немного '
                                      '*доброты* совершенно незнакомому человеку?', parse_mode=ParseMode.MARKDOWN,
                                        reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: True)
def ans(c):
    conn = sqlite3.connect('data_dobro.db', check_same_thread=False)
    u = conn.cursor()
    keyboard2 = types.InlineKeyboardMarkup()
    keyboard3 = types.InlineKeyboardMarkup()
    kb3 = types.InlineKeyboardButton(text="Готов(а)", callback_data="text3")
    kb4 = types.InlineKeyboardButton(text="Не готов(а)", callback_data="text4")
    kb5 = types.InlineKeyboardButton(text="Я с вами!", callback_data="text5")
    kb6 = types.InlineKeyboardButton(text="Пожалуй, я пас!", callback_data="text6")
    keyboard2.add(kb3, kb4)
    keyboard3.add(kb5, kb6)
    keyboard4 = types.InlineKeyboardMarkup()
    kb7 = types.InlineKeyboardButton(text="Таблица получателей", callback_data="text7")
    kb8 = types.InlineKeyboardButton(text="Таблица отправляющих", callback_data="text8")
    keyboard4.add(kb7, kb8)
    if c.data == 'text_bd':
        bot.send_message(c.message.chat.id, 'Какую таблицу Вам вывести?')
    elif c.data == 'text7':
        user_data = u.execute('select * from user_data')
        user_data = [user_data]
        bot.send_message(c.message.chat.id, user_data)
    elif c.data == 'text8':
        pass
    if c.data == "text1":
        bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=None)
        user_id = u.execute("select user_id from otvet_data where user_id = ? limit 1", (str(user),)).fetchone()
        user_id = [user_id]
        user_id = str(user_id).strip('[(\')],')
        if user_id != 'None':
            bot.send_message(c.message.chat.id, 'Вы уже приняли участие!')
        else:
            bot.send_message(c.message.chat.id,
                             '*Замечательно!*\n\nЯ знал, что на тебя можно рассчитывать.\n\n*Равнодушие - это одна из '
                             'значимых проблем современного мира и её нужно пробовать как-то решать.*\n\n*Ты спросишь '
                             'как?*\n\nВсе начинается с малого. Мы привыкли к цифровому общению. Даже с праздниками '
                             'поздравляем сообщениями в социальных сетях. Сколько тепла и ценности в этих смайликах и '
                             'пустых словах? А ты когда-нибудь отправлял(а) письма или посылки своим близким? И не '
                             'говори, что проще купить какой-нибудь сертификат и "не париться", человек сам выберет '
                             'себе, что захочет. Если такие отношения с самими дорогими, то что говорить о совершенно '
                             'незнакомых людях.\n\nЛюдям не хватает заботы и доброты в этом Мире и мои создатели '
                             'хотят попытаться это исправить.\n\n*Ты готов пойти с нами по этому пути?*')
    elif c.data == 'text3':
        bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=None)
        abonent = []
        abonent2 = []
        abonent.append(u.execute("select user from user_data limit 1").fetchone())
        abonent2.append(u.execute("select user from user_data where vozvrat = 1 limit 1").fetchone())
        pol = str(abonent).strip('[(\')],')
        pol2 = str(abonent2).strip('[(\')],')
        if pol2 == 'None':
            bot.send_message(c.message.chat.id,
                             u'*Хватит разговоров, пора переходить к действиям!*\n\n*Смотри:*\n{abonent1}\nОн(она) '
                             u'очень ждёт, чтобы ты прислал(а) ему что-то. Это может быть всё что угодно. Решать '
                             u'тебе. Цена подарка не важна, главное -  это должно быть от сердца. Ведь у каждого в '
                             u'нашей жизни есть "маленькие" радости, благодаря которым мы чувствуем себя немного '
                             u'счастливее. А еще было бы здорово, приложить к подарку письмо. Расскажи в нём: в чём '
                             u'ты сам видишь счастье. Ты можешь передумать. Это нормально. Поэтому срок на '
                             u'отправление *всего 5 дней*.\n\n*Эти рамки преследуют 2 цели:*\n1. Мы очень часто всё '
                             u'откладываем на потом. Хватит жить потом, #живисейчас.\n2. Так моим создателям будет '
                             u'проще отследить, чтобы каждый не остался без подарка.\n*Ну что? Ты с нами? Остался '
                             u'последний шаг.*'.format(
                                 abonent1=pol))
        else:
            bot.send_message(c.message.chat.id,
                             u'Хватит разговоров, пора переходить к действиям!\n\n*Смотри:*\n{abonent1}\nОн(она) '
                             u'очень ждёт, чтобы ты прислал(а) ему что-то. Это может быть всё что угодно. Решать '
                             u'тебе. Цена подарка не важна, главное -  это должно быть от сердца. Ведь у каждого в '
                             u'нашей жизни есть "маленькие" радости, благодаря которым мы чувствуем себя немного '
                             u'счастливее. А еще было бы здорово, приложить к подарку письмо. Расскажи в нём: в чём '
                             u'ты сам видишь счастье. Ты можешь передумать. Это нормально. Поэтому срок на '
                             u'отправление *всего 5 дней*.\n\nЭти рамки преследуют 2 цели:\n1. Мы очень часто всё '
                             u'откладываем на потом. Хватит жить потом, #живисейчас.\n2. Так моим создателям будет '
                             u'проще отследить, чтобы каждый не остался без подарка.\nНу что? Ты с нами? Остался '
                             u'последний шаг.'.format(
                                 abonent1=pol2))
    elif c.data == 'text5':
        bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=None)
        sent = bot.send_message(c.message.chat.id,
                                u'*Доброта спасёт Мир!*\n\nНапиши свои данные, чтобы кто-то прислал тебе подарок. ('
                                u'Обязательно нужно указать ФИО, Индекс и Адрес. Если есть желание, то можешь '
                                u'написать свой возраст, чтобы человеку было проще). Я понимаю, что персональные '
                                u'данные это очень важно, поэтому их увидит всего 1 человек, не переживай.\n\n*Не '
                                u'стесняйся, ведь всё должно возвращаться бумерангом.*')
        bot.register_next_step_handler(sent, do_end)
    elif c.data == 'text2' or c.data == 'text4' or c.data == 'text6':
        bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=None)
        bot.send_message(c.message.chat.id, 'Мы ждем тебя в следующий раз!')
    else:
        bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=None)
        bot.send_message(c.message.chat.id, 'Нажмите сюда => /start')


def do_end(message):
    conn = sqlite3.connect('data_dobro.db', check_same_thread=False)
    u = conn.cursor()
    user_id = message.from_user.id
    otvet = message.text
    abonent = []
    abonent2 = []
    abonent.append(u.execute("select user from user_data limit 1").fetchone())
    abonent2.append(u.execute("select user from user_data where vozvrat = 1 limit 1").fetchone())
    pol = str(abonent).strip('[(\')],')
    pol2 = str(abonent2).strip('[(\')],')
    data = datetime.date.today()
    data_end = data + datetime.timedelta(days=5)
    if pol2 == 'None':
        bot.send_message(message.chat.id,
                         '*Даже взмах крыльев бабочки может вызвать цунами на другом конце света.*\n\n Кто знает во '
                         'что превратится этот проект. *Крайний срок отправки: {}!* Фотографию с треком об отправке '
                         'письма с хештегом #посылкаотсердца пришли сюда: [{}](tg://user?id={}) или [{}](tg://user?id={}). '
                         'Номер трека придет '
                         'получателю, чтобы подарок точно не прошел мимо него. И запускай этот вирус в инстаграме: '
                         'Ставь хештег #посылкаотсердца, отправляй своим друзьям и отмечай в сторис.'.format(
                             str(data_end),
                             'Игорь',
                             '737181059',
                             'Васек',
                             '508015205', ))
        u.execute("insert into otvet_data(user_id, otpravitel, poluchatel, data, data_end) values (?,?,?,?,?)",
                  (user_id, otvet, pol, data, data_end))
        u.execute("delete from user_data where user_data.user = ?", (pol,))
        conn.commit()
    else:
        bot.send_message(message.chat.id,
                         '*Даже взмах крыльев бабочки может вызвать цунами на другом конце света.*\n\n Кто знает во '
                         'что превратится этот проект. *Крайний срок отправки: {}!* Фотографию с треком об отправке '
                         'письма с хештегом #посылкаотсердца пришли сюда: [{}](tg://user?id={}) или [{}](tg://user?id={}). '
                         'Номер трека придет '
                         'получателю, чтобы подарок точно не прошел мимо него. И запускай этот вирус в инстаграме: '
                         'Ставь хештег #посылкаотсердца, отправляй своим друзьям и отмечай в сторис.'.format(
                             str(data_end),
                             'Игорь',
                             '737181059',
                             'Васек',
                             '508015205', ))
        u.execute("insert into otvet_data(user_id, otpravitel, poluchatel, data, data_end) values (?,?,?,?,?)",
                  (user_id, otvet, pol2, data, data_end))
        u.execute("delete from user_data where user_data.user = ?", (pol2,))
        conn.commit()


if __name__ == '__main__':
    bot.polling(none_stop=True)
