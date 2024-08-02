import time
# from service.service import check_mail
from mail.service.service import check_mail
from obrabotka_text.service.service import main

def run_mail():
    print("Запуск сервера")
    try:
        while True:
            body = check_mail()
            if body is not None:
                print(body)
                secret_key = "secret_Ru3ArATfhvqadwy8KGZWPcJgKVDocWDIL8xvGrjt8Gh"

                url = main(secret_key= secret_key,meetgeek_transcript=body)
                print(url)
            time.sleep(1)
    except Exception as e:
        print(f'Error: {e}')
    finally:
        print("заканчиваю работу")
