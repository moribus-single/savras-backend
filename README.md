# savras-backend
# Описание
Репозиторий back-end'a для проекта Tinkoff "Savras", содержащий в себе эндпоинты для запросов с front-end'а.
Реализовано: 

- :white_check_mark: Авторизация / Регистрация
- :white_check_mark: Загрузка .xlsx файлов
- :white_check_mark: Выполнение линейной регрессии
- :white_check_mark: Удаление / Выделение аномалий
- :white_check_mark: Обычный прогноз prophet
- :white_check_mark: Нейронный прогноз neuralprophet

Промежуточные / итоговые результаты формата .xlsx сохраняются в data.

Результаты визуализации, как пример для front-end'а, сохраняются в visualisation.

# Для запуска необходимо
Python 3.10 и выше

# Инструкция по установке и запуску
1. Клонируйте репозиторий: https://github.com/moribus-single/savras-backend.git
2. Перейдите в папку savras-backend: **cd savras-backend**
3. Установите необходимые библиотеки: **pip install -r requirements.txt**
4. Запустите проект: **uvicorn main:app --reload**

# Инструкция по использованию
1. Перейдите на swagger страницу: **http://127.0.0.1:8000/docs**
2. Проверьте существующие эндпоинты и делайте свои запросы по аналогии

# Видео-демонстрация функционала
[Ссылка на youtube видео](https://www.youtube.com/watch?v=S-JuvVtbo-M)

# Контакты разработчиков
- Back-end:
  - Фадеев Тимофей tg: @f4vir0
  - Галась Данил tg: @dddnnl
  - Гришкевич Максим tg: @thethebra
- Analytics
  - Гетто Игорь tg: @igor_getto
  - Козлов Дмитрий tg: @dmitryscale5
- Visualisation
  - Алямовский Артём tg: @alyamovskiyAA
  

