# Devman Checker Lessons Bot

Telegram-бот для получения уведомлений о статусе проверки домашних заданий на платформе Devman ([https://dvmn.org](https://dvmn.org)).

Бот периодически опрашивает API Devman и отправляет уведомления в Telegram, когда работа проверена преподавателем.

> Проект выполнен в рамках курса Devman и используется в учебных целях.

---

## Возможности

* 🔔 Уведомляет о результате проверки работы
* ❌ Сообщает, если в работе есть ошибки
* ✅ Сообщает, если работа принята
* 🛠 Работает в фоне через `systemd`
* 📜 Ведёт логи и отправляет сообщения о запуске и ошибках в Telegram

---

## Требования

* Python **3.8+**
* Linux / macOS / Windows
* Аккаунт Devman
* Telegram-бот

---

## Установка и запуск (локально)

### 1. Клонировать репозиторий

```bash
git clone https://github.com/MaksimObozniy/Devman_check_lessons_bot.git
cd Devman_check_lessons_bot
```

---

### 2. Создать и активировать виртуальное окружение

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

---

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

---

### 4. Настроить переменные окружения

Создайте файл `.env` в корне проекта:

```env
LESSON_API=<API-токен Devman>
MAIN_TG_BOT_API=<API-токен основного Telegram-бота>
LOGGER_TG_BOT_API=<API-токен Telegram-бота для логгирования>
TG_CHAT_ID=<ваш chat_id>
```

#### Описание переменных:

* **LESSON_API** — персональный API-токен Devman

  * Получить: [https://dvmn.org/api/docs/](https://dvmn.org/api/docs/)

* **MAIN_TG_BOT_API** и **LOGGER_TG_BOT_API** — токены Telegram-бота

  * Получить у @BotFather

* **TG_CHAT_ID** — chat_id пользователя, которому бот будет отправлять уведомления

  * Получить через @userinfobot

---

### 5. Запуск бота

```bash
python bot.py
```

После запуска бот начнёт отслеживать статус проверки заданий и отправлять уведомления в Telegram.

---

## Запуск на сервере (production)

Проект поддерживает запуск через `systemd`:

* бот работает в фоне
* автоматически перезапускается при падении
* логирует запуск и ошибки

Основные команды:

```bash
sudo systemctl start Devman_check_lessons_bot
sudo systemctl status Devman_check_lessons_bot
sudo systemctl restart Devman_check_lessons_bot
```

Логи:

```bash
journalctl -u Devman_check_lessons_bot -f
```

---

## Логирование

Бот использует стандартный модуль `logging`:

* сообщение **"Бот запущен"** отправляется при старте
* сообщение **"Бот упал с ошибкой"** отправляется при исключениях
* traceback ошибок доступен в `journalctl`

---

## Структура проекта

```text
Devman_check_lessons_bot/
├── bot.py
├── requirements.txt
├── README.md
├── .env (не хранится в репозитории)
└── venv/
```

---

## Примечания

* Проект предназначен для одного пользователя (учебный кейс)


