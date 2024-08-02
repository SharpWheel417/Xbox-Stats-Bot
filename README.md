![Xbox](https://img.shields.io/badge/xbox-%23107C10.svg?style=for-the-badge&logo=xbox&logoColor=white)
![Xbox](https://img.shields.io/badge/stats-%23107C10.svg?style=for-the-badge&logo=xbox&logoColor=white)
![Xbox](https://img.shields.io/badge/bot-%23107C10.svg?style=for-the-badge&logo=xbox&logoColor=white)
### Xbox-Stats-Bot

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logoColor=ffdd54)

Build with https://xbl.io/

## Fast Start
1. Создайте файл config.py
2. Добавьте в него переменные:

```
BOT_TOKEN = ''
ADMIN_ID = []
```

3. Скачайте нужные библиотеки, запустив файл requirements.bat или requirements.sh в зависимости от вашей ОС

4. Запустите ``` nohup bot.py ```



## Окружение
Создаем ```python3 -m venv xlb```

Заходим ```source xlb/bin/activate```


ВАЖНО
Чтобы после отключения от сервера процесс продолжар работать запустите бота вот таким способом

```nohup python bot.py &```

nohup так же создаст файл в директории запуска nohup.out Там будут лежать логи вашего процесса

Чтобы отключить процесс

```ps aux | grep bot.py```

```kill 12345```