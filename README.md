# YoutubeParser

**YoutubeParser** – телеграм-бот для получения видео с YouTube-канала по его названию и указанию количества роликов.

## Описание

YoutubeParser позволяет пользователям ввести имя канала на YouTube и указать, сколько роликов они хотят получить (до 30). Бот извлекает актуальные ссылки на видео и отправляет их пользователю. Полезен при ограниченном доступе к YouTube, так как бот отправляет ссылки на видео напрямую.

Проект был реализован с использованием:
- Данных с [YouTube](https://www.youtube.com/)
- Платформы для хостинга [Replit](https://replit.com/)
- Библиотек Python:
  - `aiogram` для взаимодействия с Telegram API
  - `requests` для работы с HTTP-запросами к YouTube

## Структура файлов

- **main.py** – основной файл для запуска бота, обработки команд и состояний пользователей.
- **parser.py** – модуль для работы с YouTube, включая функции поиска канала и получения ссылок на видео.

## Запуск проекта
1. **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/yourusername/YoutubeParser.git
    cd YoutubeParser
    ```
3. **Создайте файл конфигурации:** В корне проекта создайте файл config.py и добавьте в него ваш токен Telegram API:

    ```python
    TOKEN = "ВАШ_ТЕЛЕГРАМ_ТОКЕН"
    ```
5. Запустите бота:

    ```bash
    python main.py
    ```
### Требования
Для работы необходим Python 3.8+ и установка следующих библиотек таким образом:

  ```bash
  pip install aiogram requests
  ```
## Использование
### Доступные команды
- /start – приветствие и начало работы с ботом.
- /help – описание основных возможностей бота.
- /get_new_videos – запрос видео по каналу, введенному пользователем.
- /cancel – отмена текущего действия.
