import telebot
import configure
from telebot import types
import random

users = {}
users_score = {'score' : '', 'count' : '', 'question': [] }
ques = {}

with open('q.txt', 'r', encoding='UTF-8') as f:
    while True:
        a = f.readline()[:-1]
        if not a:
            break
        b = f.readline()[:-1]
        ques[a] = b

client = telebot.TeleBot(configure.config['token'])

@client.message_handler(commands = ['start'])
def start_vic(message):
    """
    Отвечает на команду /start
    :param message: принимает
    :return: приветствие, кнопку для запуска викторины
    """
    murkup_inline = types.InlineKeyboardMarkup()
    item_vic = types.InlineKeyboardButton(text = 'начать викторину',callback_data='vic')

    murkup_inline.add(item_vic)
    users[message.chat.id] = users_score.copy()   # запоминаем id юзера
    users[message.chat.id]['score'] = 0     # задаем ему счет
    users[message.chat.id]['count'] = 3     # задаем кол-во оставшихся вопросов
    client.send_message(message.chat.id, 'Привет! Эта викторина будет состоять из 3х вопросов. Нажми на кнопочку, чтобы начать викторину',
                        reply_markup=murkup_inline)

@client.callback_query_handler (func=lambda call: call.data == "vic")
def question1(call):
    """
    Задаем рандомные вопросы
    :param call: сообщение, которое передаем функции
    :return: запуск finish, question2 или questionf в зависимости от кол-ва оставшихся вопросов
    """
    if users[call.message.chat.id]['count'] <= 0:  # если все вопросы задали, то завершаем викторину
        finish(call.message.chat.id)
    else:            # иначе продолжаем задавать вопросы
        users[call.message.chat.id]['count'] -= 1
        que, ans = random.choice(list(ques.items()))  # выбираем рандомный вопрос из словаря вопросов
        while que in users[call.message.chat.id]['question']: # проверяем не задавали ли его до этого
            que, ans = random.choice(list(ques.items()))

        users[call.message.chat.id]['question'].append(que)
        msg = client.send_message(call.message.chat.id, que)
        if users[call.message.chat.id]['count'] <= 0:
            client.register_next_step_handler(msg, questionf, call.message.chat.id, ans)
        else:
            client.register_next_step_handler(msg, question2, call.message.chat.id, ans)

def question2(call, id, ans):
    """
    Проверяет правильность ответа пользователя
    :param call: сообщение, которое передаем функции
    :param id: id пользователя
    :param ans: правильный ответ на вопрос
    :return: кнопки для перехода к следующему вопросу или для завершения викторины; запускает try_again при неправильном ответе
    """
    murkup_inline = types.InlineKeyboardMarkup()
    item_vic = types.InlineKeyboardButton(text='К следующему вопросу', callback_data='vic')
    item_nea = types.InlineKeyboardButton(text='Закончить викторину', callback_data='nea')
    murkup_inline.add(item_vic, item_nea)
    if call.text.lower() == ans.lower():
        users[id]['score'] += 1
        msg = client.send_message(id, 'Умничка! Это правильный ответ', reply_markup=murkup_inline)
    else:
        msg = client.send_message(id, 'Неа, попробуй еще раз')
        client.register_next_step_handler(msg, try_again, id, ans)

def try_again(call, id, ans):
    """
    Проверяет правильность ответа на вторую попытку
    :param call: сообщение, которое передаем функции
    :param id: id пользователя
    :param ans: правильный ответ на вопрос
    :return: кнопки для перехода к следующему вопросу или для завершения викторины
    """
    murkup_inline = types.InlineKeyboardMarkup()
    item_vic = types.InlineKeyboardButton(text='К следующему вопросу', callback_data='vic')
    item_nea = types.InlineKeyboardButton(text='Закончить викторину', callback_data='nea')
    murkup_inline.add(item_vic, item_nea)
    if call.text.lower() == ans.lower():
        users[id]['score'] += 1
        msg = client.send_message(id, 'Умничка! Это правильный ответ', reply_markup=murkup_inline)
    else:
        msg = client.send_message(id, 'Нет, правильный ответ: ' + ans, reply_markup=murkup_inline)

def questionf (call, id, ans):
    """
    Проверяет правильность последнего вопроса
    :param call: сообщение, которое передаем функции
    :param id: id пользователя
    :param ans: правильный ответ на вопрос
    :return: кнопку для перехода к результатам
    """
    murkup_inline = types.InlineKeyboardMarkup()
    item_vic = types.InlineKeyboardButton(text='К результатам', callback_data='vic')
    murkup_inline.add(item_vic)

    if call.text.lower() == ans.lower():
        users[id]['score'] += 1
        msg = client.send_message(id, 'Абсолютно верно!', reply_markup=murkup_inline)
    else:
        msg = client.send_message(id, 'Неа, верный ответ: ' + ans, reply_markup=murkup_inline)

@client.callback_query_handler (func=lambda call: call.data == "nea")
def nea1(call):
    """
    Подтверждение завершения викторины
    :param call: сообщение, которое передаем функции
    :return: кнопки для прехода к результатам, возвращения к викторине
    """
    murkup_inline = types.InlineKeyboardMarkup()
    item_vic = types.InlineKeyboardButton(text='Нет, хочу продолжить викторину', callback_data='nea_vic')
    item_nea = types.InlineKeyboardButton(text='Да, к результатам', callback_data='nea2')
    murkup_inline.add(item_vic, item_nea)
    msg = client.send_message(call.message.chat.id, 'Уверен?', reply_markup=murkup_inline)

@client.callback_query_handler (func=lambda call: call.data == "nea2")
def nea2(call):
    """
    Вызов функции для завершения викторины после подтверждения
    :param call: сообщение, которое передаем функции
    :return: finish
    """
    finish(call.message.chat.id)

@client.callback_query_handler (func=lambda call: call.data == "nea_vic")
def nea_vic(call):
    """
    Для продолжения викторины
    :param call: сообщение, которое передаем функции
    :return: кнопки для получения вопроса, окончания викторины
    """
    murkup_inline = types.InlineKeyboardMarkup()
    item_vic = types.InlineKeyboardButton(text='Узнать вопрос', callback_data='vic')
    item_nea = types.InlineKeyboardButton(text='Закончить викторину', callback_data='nea')
    murkup_inline.add(item_vic, item_nea)
    msg = client.send_message(call.message.chat.id, 'Супер! Тогда давай продолжать', reply_markup=murkup_inline)

def finish( id):
    """
    Завершает викторину
    :param id: id пользователя
    :return: Результаты викторины, пояснения для команд /pay и /start
    """
    if users[id]['score'] == 0:
        client.send_message(id, "Ты не ответил правильно ни на один вопрос!")
    elif (users[id]['score']) == 1:
        client.send_message(id, "Ты ответил на один вопрос из трех. Неплохо.")
    elif (users[id]['score']) == 2:
        client.send_message(id, "Поздравляю, целых два правильных ответа!")
    elif (users[id]['score']) == 3:
        client.send_message(id, "Вау! Ты ответил правильно на все вопросы! Поздравляю!")
    client.send_message(id, "Чтобы запустить викторину заново нажми /start")
    client.send_message(id, "Также ты можешь поддержать разработчика, нажав /pay")

@client.message_handler(commands=['pay'])
def pay(msg):
    """
    Для поддержки разработчика
    :param msg: передаем
    :return: Куда скинуть денюшку
    """
    client.send_message(msg.chat.id, "qiwi.com/n/ASSISTINADM")

if __name__ == '__main__':
    client.polling(none_stop=True, interval=0)