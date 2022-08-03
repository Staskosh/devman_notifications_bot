# Уведомления о результатах проверки уроков Девман
Данный скрипт позволяет получать уведомления по результатам проверки уроков на сайте [Девман](https://dvmn.org/modules/) 


### Как установить

Создайте бота и получите токен.
Сделать это можно тут: [BotFather](https://telegram.me/BotFather), для этого необходимо
ввести `/start` и следовать инструкции.

Запустите полученного бота при помощи команды `/start`.

Далее рядом с кодом вы должны создать файл `.env`, в котором будут храниться
ваши личные данные:

```
TG_TOKEN='Токен телеграм бота'
DEVMAN_TOKEN='обратитесь к поддержку Девман для получения'
TG_CHAT_ID='Ваш чат id'
```

[Python3]('https://www.python.org/downloads/') и [виртуальное окружение]('https://python-scripts.com/virtualenv') должны быть установлены.
### Как запустить
1. Скачайте код
2. Установите зависимости командой:
```bash
pip install -r requirements.txt
```
3. Чтобы получить свой chat_id, напишите в Telegram специальному боту: `@userinfobot`:
   
4. Запустите скрипт:
```bash
python3 get_devman_notifications.py
```
### Как запустить на Хероку
1. Зарегистрируйтесь на [Хероку](https://id.heroku.com/login)
2. Cоздайте приложение (app). 
3. Привяжете аккаунт GitHub к аккаунту Heroku во вкладке Deploy и нажмите Deploy Branch.
4. Заполните чувствительные данные Config Vars из файла `.env` во вкладке Settings.
5. Активируйте Dyno во вкладке Resources. 

Готово, теперь ваш бот будет работать постоянно.

### Создание контейнера Docker:

#### Запуск на локальной машине:
1. Создайте образ:
```bash
docker build -t devman_notification_bot_docker . 
```
2. Запустите образ локально:
```bash
docker run -d --env-file ./.env devman_notification_bot_docker 
```
Подробнее смотрите [документацию](https://docs.docker.com/get-started/).

#### Как запустить контейнер на Хероку
1. Зарегистрируйтесь на [Хероку](https://id.heroku.com/login)
2. Cоздайте приложение (app). 
3. Выберите Deployment method во вкладке Deploy.
4. Следуйте инструкциям ниже в пункте Deploy your Docker-based app.
5. Заполните чувствительные данные Config Vars из файла .env во вкладке Settings.
6. Активируйте Dyno во вкладке Resources.

Если в результате запуска вы получили ошибку, то можно воспользоваться методом ниже.
(Проверено только для Macbook c M1)

1. Создайте образ:
```bash
docker buildx build --load --platform linux/amd64 -t registry.heroku.com/app_name/bot -a app_name
```
2. Отправьте образ:
```bash
docker push registry.heroku.com/app_name/bot:latest -a app_name
```
3. Запустите образ на Хероку:
```bash
heroku container:release bot -a app_name
```
