# savras-backend
# Описание
Репозиторий back-end'a для проекта Tinkoff "Savras", содержащий в себе эндпоинты для запросов с front-end'а.
Реализована функция авторизации

# Для запуска необходимо
Python 3.10 и выше

# Инструкция по установке и запуску
1. Клонируйте репозиторий: https://github.com/moribus-single/savras-backend.git
2. Перейдите в папку savras-backend: **cd savras-backend**
3. Перейдите в venv: .\venv\Scripts\activate
4. Установите необходимые библиотеки: **pip install -r requirements.txt**
5. Запустите проект: **uvicorn main:app --reload**

# Инструкция по использованию
1. Перейдите на swagger страницу: **http://127.0.0.1:8000/docs**
2. Проверьте существующие эндпоинты и делайте свои запросы по аналогии
