import argparse
import os

import requests
import telegram
from dotenv import load_dotenv


def send_message(tg_token, api_answer, tg_chat_id):
    bot = telegram.Bot(token=tg_token)
    lesson_info = api_answer['new_attempts'][0]
    lesson_title = lesson_info['lesson_title']
    lesson_url = lesson_info['lesson_url']
    check_result = 'Ваша работа принята!'
    if lesson_info['is_negative'] is True:
        check_result = 'К сожалению, в работе нашлись улучшения.'
    message = f'Преподаватель проверил работу "{lesson_title}"! \n' \
              f'Ссылка на работу \n {lesson_url} \n' \
              f'{check_result}'
    bot.send_message(text=message, chat_id=tg_chat_id)


def get_devman_lessons_updates(devman_token, tg_token, tg_chat_id):
    long_poling_url = 'https://dvmn.org/api/long_polling/'
    timestamp = None
    headers = {'Authorization': f'Token {devman_token}'}
    while True:
        try:
            payload = {'timestamp': timestamp}
            request = requests.get(long_poling_url, headers=headers, params=payload)
            request.raise_for_status()
            api_answer = request.json()
            request_status = api_answer['status']
            if request_status == 'found':
                send_message(tg_token, api_answer, tg_chat_id)
            if request_status == 'timeout':
                timestamp = api_answer['timestamp_to_request']
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            print(e)


def main():
    load_dotenv()
    devman_token = os.getenv('DEVMAN_TOKEN')
    tg_token = os.getenv('TG_TOKEN')
    parser = argparse.ArgumentParser()
    parser.add_argument("tg_chat_id", help="Enter the telegram chart id",
                        type=str)
    args = parser.parse_args()
    get_devman_lessons_updates(devman_token, tg_token, args.tg_chat_id)


if __name__ == '__main__':
    main()
