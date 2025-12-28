import os
import time
import logging

from telegram import Bot
import requests
from requests.exceptions import ReadTimeout, ConnectionError
from dotenv import load_dotenv


class TelegramLogsHandler(logging.Handler):
    def emit(self, record):
        log_message = self.format(record)
        logs_bot.send_message(chat_id=tg_chat_id, text=log_message)


def main():
    global logs_bot, tg_chat_id

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s — %(levelname)s — %(message)s",
    )

    try:
        load_dotenv()

        tg_chat_id = os.environ["TG_CHAT_ID"]
        lesson_api = os.environ["LESSON_API"]
        main_tg_bot_api = os.environ["MAIN_TG_BOT_API"]
        logger_tg_bot_api = os.environ["LOGGER_TG_BOT_API"]

        main_bot = Bot(token=main_tg_bot_api)
        logs_bot = Bot(token=logger_tg_bot_api)

        telegram_handler = TelegramLogsHandler()
        telegram_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")
        telegram_handler.setFormatter(formatter)

        logging.getLogger().addHandler(telegram_handler)
        logging.getLogger("telegram").setLevel(logging.WARNING)

        logging.info("Бот запущен")

        reviews_url = "https://dvmn.org/api/long_polling/"
        headers = {"Authorization": f"Token {lesson_api}"}
        timestamp = None

        while True:
            try:
                params = {"timestamp": timestamp} if timestamp else {}
                response = requests.get(reviews_url, headers=headers, params=params, timeout=60)
                response.raise_for_status()
                review_info = response.json()

                if review_info["status"] == "found":
                    for attempt in review_info["new_attempts"]:
                        lesson_title = attempt["lesson_title"]
                        lesson_url = attempt["lesson_url"]

                        if attempt["is_negative"]:
                            main_bot.send_message(
                                chat_id=tg_chat_id,
                                text=(
                                    f"У вас проверили работу «{lesson_title}»!\n"
                                    f"К сожалению, в работе нашлись ошибки.\n"
                                    f"Ссылка на работу: {lesson_url}"
                                ),
                            )
                        else:
                            main_bot.send_message(
                                chat_id=tg_chat_id,
                                text=(
                                    f"У вас проверили работу «{lesson_title}»!\n"
                                    f"Преподавателю всё понравилось, можно приступать к следующему уроку!\n"
                                    f"Ссылка на работу: {lesson_url}"
                                ),
                            )

                    timestamp = review_info["last_attempt_timestamp"]

                elif review_info["status"] == "timeout":
                    timestamp = review_info["timestamp"]

            except ReadTimeout:
                continue
            except ConnectionError:
                time.sleep(10)

    except Exception:
        logging.exception("Бот упал с ошибкой :")
        raise


if __name__ == "__main__":
    main()
