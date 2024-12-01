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
        print("Для остановки работы клиента нажмите Ctrl + C или Ctrl + Z")
        run_client()
    except KeyboardInterrupt:
        print("\nКлиент остановлен.")

