import os

import telebot
import sqlite3
import datetime

from telebot import types
from dotenv import load_dotenv
from telegram.constants import ParseMode

load_dotenv()

bot = telebot.TeleBot(os.getenv('BOT_KEY'))

user = None


@bot.message_handler(commands=['start'])
def start_message(message):
    global user
    user = message.from_user.id
    keyboard = types.InlineKeyboardMarkup()
    kb1 = types.InlineKeyboardButton(text="Давай попробуем!", callback_data="text1")
    kb2 = types.InlineKeyboardButton(text="Пожалуй, нет!", callback_data="text2")
    keyboard.add(kb1, kb2)
    bot.send_message(message.chat.id, '*Привет!*🤗\nМеня создали для того, чтобы *МЫ* 👨‍👩‍👦‍👦 участники нашего '
                                      'коммьюнити '
                                      '*TuvaGames* почувствовали себя немного *счастливее*🔥. Однажды каждый осознанный '
                                      'человек приходит к простому выводу: жить с позиции *\"отдавать\"* '
                                      'намного приятнее , чем с позиции *\"брать\"*.\n\nМожет попробуем подарить '
                                      'немного *доброты* друг другу?🤝',
                     reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)


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
    if c.data == "text1":
        bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=None)
        user_id = u.execute("select id_receiver from users where id_receiver = ? limit 1", (str(user),)).fetchone()
        # вывожу юзера который пользуется ботом
        user_id = [user_id]
        user_id = str(user_id).strip('[(\')],')
        #  записал в user_id
        if user_id != 'None':  # проверяю есть ли пользователь уже в таблице
            bot.send_message(c.message.chat.id, 'Вы уже приняли участие!')
        else:  # если нет, то продолжаем диалог
            bot.send_message(c.message.chat.id,
                             '*Замечательно!*✔\n\nЯ знал, что на тебя можно рассчитывать.❤\n\n*Равнодушие😐 - это '
                             'одна из '
                             'значимых проблем современного мира и её нужно пробовать как-то решать.👆*\n\n*Ты спросишь '
                             'как?*\n\nВсе начинается с малого. Мы привыкли к цифровому общению.📱 Даже с праздниками '
                             'поздравляем сообщениями в социальных сетях. Сколько тепла и ценности в этих смайликах и '
                             'пустых словах? А ты когда-нибудь отправлял(а) письма или посылки своим близким? И не '
                             'говори, что проще купить какой-нибудь сертификат и "не париться", человек сам выберет '
                             'себе, что захочет. Если такие отношения с самими дорогими, то что говорить о совершенно '
                             'незнакомых или малознакомых людях.\n\nЛюдям не хватает заботы и доброты в этом Мире '
                             'и мы хотим попытаться это исправить.\n\n*Ты готов пойти с нами по этому пути?*🔥',
                             reply_markup=keyboard2, parse_mode=ParseMode.MARKDOWN)
    elif c.data == 'text3':  # если положительный ответ, то делимся юзернэйм, кому дарить придется подарок
        bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=None)
        abonent = [u.execute("select id_receiver from users order by timestamp desc limit 1").fetchone()]
        abonent = str(abonent).strip('[(\')],')
        info = [u.execute("select receiver from users order by timestamp desc limit 1").fetchone()]
        info = str(info).strip('[(\')],')
        bot.send_message(c.message.chat.id,
                         u'*Хватит разговоров, пора переходить к действиям!*\n\n*Смотри:*\ntg://user?id={abonent}'
                         u'\n{info}\n\n'
                         u'Он(она) очень ждёт, чтобы ты прислал(а) ему что-то.🎁 Это может быть всё что угодно. Решать '
                         u'тебе. Цена подарка не важна🤑, главное -  это должно быть от сердца💘. Ведь у каждого в '
                         u'нашей жизни есть "маленькие" радости, благодаря которым мы чувствуем себя немного '
                         u'счастливее. А еще было бы здорово, приложить к подарку письмо.💌 Расскажи в нём: в чём '
                         u'сам видишь счастье. Ты можешь передумать. Это нормально. Поэтому срок на '
                         u'отправление *всего 10 дней*.⌛\n\n*Эти рамки преследуют 2 цели:*\n1. Мы очень часто всё '
                         u'откладываем на потом. Хватит жить потом, #живисейчас.\n2. Так моим создателям будет '
                         u'проще отследить, чтобы никто не остался без подарка.\n*Ну что? Ты с нами? Остался '
                         u'последний шаг.*'.format(
                             abonent=abonent, info=info), reply_markup=keyboard3, parse_mode=ParseMode.MARKDOWN)

    elif c.data == 'text5':  # если ответ положительный, то просим оставить свои данные
        bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=None)
        sent = bot.send_message(c.message.chat.id,
                                u'*Доброта спасёт Мир🗺!*\n\nНапиши свои данные, чтобы кто-то прислал тебе подарок. ('
                                u'Обязательно нужно указать ФИО, Индекс и Адрес. Если есть желание, то можешь '
                                u'написать свои увлечения или намекнуть на что-то, чтобы ему было проще в '
                                u'выборе).\n *Например: Иванов Иван Иванович, 667000, Респ.Тыва, г.Кызыл, ул.Кочетова, '
                                u'36, кв.15. Обожаю книги и путешествия. А также люблю тортики.*\n\n*Не '
                                u'стесняйся, ведь всё должно возвращаться бумерангом.*🍆', parse_mode=ParseMode.MARKDOWN)
        bot.register_next_step_handler(sent, do_end)
    elif c.data == 'text2' or c.data == 'text4' or c.data == 'text6':  # если отказ на одном из шагов
        bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=None)
        bot.send_message(c.message.chat.id, 'Мы ждем тебя в следующий раз!')
    else:  # если уклонились от алгоритма
        bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=None)
        bot.send_message(c.message.chat.id, 'Нажмите сюда => /start')


def do_end(message):
    conn = sqlite3.connect('data_dobro.db', check_same_thread=False)
    u = conn.cursor()
    user_id = message.from_user.id
    otvet = message.text
    abonent = [u.execute("select id_receiver from users order by timestamp desc limit 1").fetchone()]
    abonent = str(abonent).strip('[(\')],')
    data = datetime.date.today()
    data_end = data + datetime.timedelta(days=10)
    timestamp = datetime.datetime.now()
    bot.send_message(message.chat.id,
                     '*Даже взмах крыльев бабочки🦋 может вызвать цунами🌊 на другом конце света.*\n\n Кто знает во '
                     'что превратится этот проект! Давай договоримся, что до *{}* ты отправишь подарок.'
                     ' Трек об отправке и фото письма с хештегом #посылкаотсердца пришли мне: '
                     '[{}](tg://user?id={}). '
                     'Номер трека придет '
                     'получателю, чтобы подарок точно не прошел мимо него. И запускай этот вирус в соц.сетях: '
                     'Ставь хештег #посылкаотсердца, отправляй своим друзьям и отмечай в сторис.'.format(
                         str(data_end),
                         'Илья Кудрин',
                         '737181059', ), parse_mode=ParseMode.MARKDOWN)
    u.execute("insert into users(id_receiver, receiver, timestamp) values (?,?,?)",
              (user_id, otvet, timestamp))
    u.execute("insert into transmit(id_transmitter, id_receiver) values (?,?)",
              (user_id, abonent))
    conn.commit()


if __name__ == '__main__':
    bot.polling(none_stop=True)
