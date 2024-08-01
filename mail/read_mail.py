import time
# from service.service import check_mail
from mail.service.service import check_mail


def run_mail():
    print("Запуск сервера")
    try:
        while True:
            check_mail()
            time.sleep(1)
    except Exception as e:
        print(f'Error: {e}')
    finally:
        print("заканчиваю работу")
