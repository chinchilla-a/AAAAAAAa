import unittest
from unittest import mock
from unittest.mock import MagicMock, ANY, call
import bot1


class Telegram_test(unittest.TestCase):
    @mock.patch('bot1.client')
    def test_vic(self, MockClient):
        name = 'test'
        user = MagicMock(first_name=name)
        chat = MagicMock(id=123)
        message = MagicMock(from_user=user, chat=chat)
        MockClient.get_me.return_value = MagicMock(first_name='bot')
        bot1.start_vic(message)
        calls = [call(123, "Привет! Эта викторина будет состоять из 3х вопросов. Нажми на кнопочку, чтобы начать викторину", reply_markup=ANY)]
        MockClient.send_message.assert_has_calls(calls)

    @mock.patch('bot1.client')
    def test_pay(self, MockClient):
        name = 'test'
        user = MagicMock(first_name=name)
        chat = MagicMock(id=123)
        message = MagicMock(from_user=user, chat=chat)
        MockClient.get_me.return_value = MagicMock(first_name='bot')
        bot1.pay(message)
        calls = [call(123, "qiwi.com/n/ASSISTINADM")]
        MockClient.send_message.assert_has_calls(calls)

    @mock.patch('bot1.client')
    def test_nea_vic(self, MockClient):
        name = 'test'
        user = MagicMock(first_name=name)
        chat = MagicMock(id=123)
        message = MagicMock(from_user=user, chat=chat)
        MockClient.get_me.return_value = MagicMock(first_name='bot')
        bot1.nea_vic(message)
        calls = [call(123, "Супер! Тогда давай продолжать", reply_markup=ANY)]
        MockClient.send_message.assert_has_calls(calls)