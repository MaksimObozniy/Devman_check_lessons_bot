import os
import time

from telegram import Bot
import requests
from requests.exceptions import ReadTimeout, ConnectionError
from dotenv import load_dotenv


def main():

    load_dotenv()

    tg_chat_id = os.environ["TG_CHAT_ID"]
    lesson_api = os.environ["LESSON_API"]
    tg_bot_token = os.environ["TG_BOT_API_TOKEN"]

    bot = Bot(token=tg_bot_token)

    reviews_url = "https://dvmn.org/api/long_polling/"
    headers ={"Authorization":f"Token {lesson_api}"}
    timestamp = None

    while True:
        try:
            params = {"timestamp": timestamp} if timestamp else {}
            response = requests.get(reviews_url, headers=headers, params=params, timeout=60)
            response.raise_for_status()

            review_info = response.json()

            if review_info['status'] == 'found':
                for attempt in review_info['new_attempts']:
                    lesson_title = attempt['lesson_title']
                    lesson_url = attempt['lesson_url']

                    if attempt['is_negative']:
                        bot.send_message(
                            chat_id=tg_chat_id,
                            text=(
                                f"У вас проверили работу «{lesson_title}»!\n"
                                f"К сожалению, в работе нашлись ошибки.\n"
                                f"Ссылка на работу: {lesson_url}"
                            )
                        )

                    else:
                        bot.send_message(
                            chat_id=tg_chat_id,
                            text=(
                                f"У вас проверили работу «{lesson_title}»!\n"
                                f"Преподавателю всё понравилось, можно приступать к следующему уроку!\n"
                                f"Ссылка на работу: {lesson_url}"
                            )
                        )

                timestamp = review_info["last_attempt_timestamp"]

            elif review_info["status"] == "timeout":
                timestamp = review_info["timestamp"]

        except ReadTimeout:
            continue

        except ConnectionError as e:
            time.sleep(10)


if __name__ == "__main__":
    main()

