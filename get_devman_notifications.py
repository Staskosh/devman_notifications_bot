import argparse
import os
import textwrap
import time

import requests
import telegram
from dotenv import load_dotenv


def send_message(bot, api_answer, tg_chat_id):
    lesson_info = api_answer['new_attempts'][0]
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


def get_devman_lessons_updates(devman_token, bot, tg_chat_id):
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
                timestamp = response['last_attempt_timestamp']
                send_message(bot, response, tg_chat_id)
            if review_status == 'timeout':
                timestamp = response['timestamp_to_request']
        except requests.exceptions.ReadTimeout as e:
            print(e)
        except requests.exceptions.ConnectionError:
            time.sleep(10)


def main():
    load_dotenv()
    devman_token = os.getenv('DEVMAN_TOKEN')
    tg_token = os.getenv('TG_TOKEN')
    bot = telegram.Bot(token=tg_token)
    parser = argparse.ArgumentParser()
    parser.add_argument("tg_chat_id", help="Enter the telegram chart id")
    args = parser.parse_args()
    get_devman_lessons_updates(devman_token, bot, args.tg_chat_id)


if __name__ == '__main__':
    main()