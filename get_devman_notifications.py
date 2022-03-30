import logging
import os
import textwrap
import time

import requests
import telegram
from dotenv import load_dotenv

tg_logger = logging.getLogger("tg_bot_notification")


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def send_message(bot, reviews, tg_chat_id):
    lesson_info = reviews['new_attempts'][0]
    lesson_title = lesson_info['lesson_title']
    lesson_url = lesson_info['lesson_url']
    check_result = 'Ваша работа принята!'
    if lesson_info['is_negative']:
        check_result = 'К сожалению, в работе нашлись улучшения.'
    message = textwrap.dedent(
        f'''
        Преподаватель проверил работу "{lesson_title}"!
        Ссылка на работу {lesson_url}
        {check_result}
        '''
    )
    bot.send_message(text=message, chat_id=tg_chat_id)


def get_devman_lessons_updates(devman_token, bot, tg_chat_id, tg_logger):
    long_poling_url = 'https://dvmn.org/api/long_polling/'
    timestamp = None
    headers = {'Authorization': f'Token {devman_token}'}
    while True:
        try:
            payload = {'timestamp': timestamp}
            response = requests.get(long_poling_url, headers=headers, params=payload)
            response.raise_for_status()
            reviews = response.json()
            review_status = reviews['status']
            if review_status == 'found':
                timestamp = reviews['last_attempt_timestamp']
                send_message(bot, reviews, tg_chat_id)
            if review_status == 'timeout':
                timestamp = reviews['timestamp_to_request']
        except requests.exceptions.ReadTimeout as e:
            print(e)
        except requests.exceptions.ConnectionError:
            time.sleep(10)


def main():
    load_dotenv()
    devman_token = os.getenv('DEVMAN_TOKEN')
    tg_token = os.getenv('TG_TOKEN')
    bot = telegram.Bot(token=tg_token)
    tg_chat_id = os.getenv('TG_CHAT_ID')
    tg_logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler("tg_bot_notification.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    tg_logger.addHandler(file_handler)
    tg_logger.addHandler(TelegramLogsHandler(bot, tg_chat_id))

    while True:
        try:
            get_devman_lessons_updates(devman_token, bot, tg_chat_id, tg_logger)
        except ZeroDivisionError as e:
            tg_logger.info('Бот упал с ошибкой')
            tg_logger.info(e)


if __name__ == '__main__':
    main()
