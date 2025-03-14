# Лабораторная работа по серверу и линуксу
## Основные шаги
1. Создать FIFO-файл для передачи сообщений между клиентом и сервером (to_desk).
2. Клиент:
  - Пишет сообщение ping в FIFO to_desk.
  - Читает ответ pong из FIFO to_desk.
  - В случае ошибки возвращается в начальную точку.
3. Сервер:
  - Читает запрос из FIFO to_desk.
  - Отвечает pong через FIFO to_desk.
  - При ошибке возвращается к ожиданию запроса.

### Реализация
Подготовка FIFO\
Перед самым первые в жизни запуском необходимо создать FIFO-файл. Выполните следующую команду в терминале:
```
mkfifo to_desk
```

Если вы уже писали предыдущую строку, то больше создавать файл to_desk не надо

Сервер (server.py)
```
def run_server(descriptor_file = "to_desk"):
    """Функция для работы сервера, она считывает запрос от клиента и посылает соответствующий ответ."""
    print("Сервер запущен и ожидает запросов...")
    while True:
        try:
            # Чтение из FIFO файла дескриптора
            with open(descriptor_file, "r") as server_fifo:
                """ Открытие файла-дескриптора для просмотра запроса от клиента"""
                request = server_fifo.read().strip()
                print(f"Получен запрос: {request}")

                # Если запрос тот, который мы хотим 
                if request == "ping":
                    response = "pong"
                    # Запись ответа в FIFO файл дескриптор
                    with open(descriptor_file, "w") as client_fifo:
                        client_fifo.write(response)
                        print(f"Отправлен ответ: {response}")
                else:
                    print(f"Ошибка: неизвестный запрос '{request}'")
        except Exception as e:
            print(f"Ошибка сервера: {e}")
            continue

if __name__ == "__main__":
    try:
        print("Для остановки сервера нажмите Ctrl + C")
        run_server()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
```

Клиент (client.py)
```
import time

def run_client(descriptor_file = "to_desk"):
    """Функция запуска работы клиента, она отправляет запрос на сервер (ping) и ждёт от него ответа (pong)"""
    print("Клиент запущен.")

    while True:
        try:
            # Отправка запроса
            request = "ping"
            with open(descriptor_file, "w") as server_fifo:
                """ Открытие файла-дескриптора для отправки запроса и закрытие его для того, чтобы с ним мог работать сервер."""
                server_fifo.write(request)
                print(f"Отправлен запрос: {request}")

            # Чтение ответа
            with open(descriptor_file, "r") as client_fifo:
                """ Открытие файла-дескриптора для чтения ответа от сервера"""
                response = client_fifo.read().strip()
                print(f"Получен ответ: {response}")
            
            # Если сервер послал не то, что мы хотим
            if response != "pong":
                print("Ошибка: неверный ответ. Повтор запроса...")
                time.sleep(1)
                continue

            # Успешное завершение
            if input("Отправить ещё раз запрос на сервер (y/n)? ").strip().lower() != "y": # .strip() - удаляет лишние пробелы; .lower() -  переводит любой регистр в нижний
                break
        except Exception as e:
            print(f"Ошибка клиента: {e}")
            time.sleep(1)
            continue

if __name__ == "__main__":
    try:
        print("Для остановки работы клиента нажмите Ctrl + C")
        run_client()
    except KeyboardInterrupt:
        print("\nКлиент остановлен.")
```

### Объяснение
1. FIFO-файл:
  - to_desk: Клиент пишет запросы, сервер читает или Сервер пишет ответы, клиент читает.
2. Сервер:
  - Ожидает запроса в цикле.
  - Если запрос равен ping, отвечает pong.
  - При ошибках продолжает ожидать запросов.
3. Клиент:
  - Пишет ping в FIFO.
  - Читает ответ.
При ошибке (например, сервер не отвечает или ответ неверен) повторяет запрос.

### Как запустить
1. Создайте FIFO:
  - mkfifo to_desk (если не делали этого раньше)
2. Запустите сервер в одном терминале:
  - python3 server.py
3. Запустите клиента в другом терминале:
  - python3 client.py
