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
        print("Для остановки сервера нажмите Ctrl + C или Ctrl + Z")
        run_server()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
