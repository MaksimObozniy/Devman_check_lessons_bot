import os
import time

import asyncio
import telegram
import requests
from requests.exceptions import ReadTimeout, ConnectionError
from dotenv import load_dotenv

load_dotenv()


async def main(tg_bot_token, tg_chat_id, api_devman):
    bot = telegram.Bot(token=tg_bot_token)

    reviews_url = "https://dvmn.org/api/long_polling/"

    headers ={
        "Authorization":f"Token {api_devman}"
        }

    timestamp = None
    while True:
        try:
            params = {"timestamp": timestamp} if timestamp else {}
            response = requests.get(reviews_url, headers=headers, params=params, timeout=90)
            response.raise_for_status()

            review_info = response.json()
            print(review_info)

            if review_info['status'] == 'found':
                for attempt in review_info['new_attempts']:
                    if attempt['is_negative'] == True:
                        await bot.send_message(
                            chat_id=tg_chat_id,
                            text=f"""У вас проверили работу '{review_info['new_attempts'][0]['lesson_title']}'!
                            \nК сожалению в работе нашлись ошибки.
                            \nСсылка на работу:\n{review_info['new_attempts'][0]['lesson_url']}""",
                        )
                    else:
                        await bot.send_message(
                            chat_id=tg_chat_id,
                            text=f"""У вас проверили работу '{review_info['new_attempts'][0]['lesson_title']}'!
                            \nПреподавателю все понравилось, можно приступать к следующему уроку!
                            \nСсылка на работу:\n{review_info['new_attempts'][0]['lesson_url']}""",
                        )

                timestamp = review_info["last_attempt_timestamp"]

            elif review_info["status"] == "timeout":
                timestamp = review_info["timestamp"]

        except ReadTimeout:
            print("Проверенных работ пока нет.")

        except ConnectionError as e:
            print("Сервер не отвечает: ", e)
            time.sleep(10)


if __name__ == "__main__":
    tg_chat_id = os.environ.get("TG_CHAT_ID")
    api_devman = os.environ.get("API_DEVMAN")
    tg_bot_token = os.environ.get("TG_BOT_API_TOKEN")

    if tg_bot_token == None:
        print("Не удается получить токен.")
    else:
        asyncio.run(main(tg_bot_token, tg_chat_id, api_devman))

