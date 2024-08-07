import time
# from service.service import check_mail
from mail.service.service import check_mail
from obrabotka_text.service.service import main
from obrabotka_text.utils.url_to_page_id import url_to_id
from notion.utils.create_comment import create_comment
from obrabotka_text.utils.text_compression import compress_text
from for_user.utils.json_to_variable import get_config_value
from mail.utils import treatment_mail
from mail.utils.string_to_email import string_to_email
from obrabotka_text.utils.obrezka_text import extract_text_between_timestamps


def run_mail():
    k = 0
    print("Запуск сервера", flush=True)
    try:
        while True:
            body = check_mail()
            body_save = body
            # body_save = extract_text_between_timestamps(body_save) этот код обрезает
            if body_save is not None:
                body_mas = extract_text_between_timestamps(body)  # это массив
                # print(body)
                secret_key = get_config_value('secret_key')

                # проверка пользователя
                string_email = string_to_email(treatment_mail.from_)
                # if string_email == "app@meetgeek.ai":
                if string_email == "crymov.artyom@yandex.ru":
                    # получение ссылки
                    for i in body_mas:
                        url = main(secret_key=secret_key, meetgeek_transcript=i)
                        page_id = url_to_id(url)
                        body_save = compress_text(i)

                        # print(f"{treatment_mail.from_}")
                        create_comment(page_id, i)
                else:
                    print("Недопустимый email")

            # алгоритм для индикации запуска сервера
            if k == 0:
                # print(k, flush=True)
                print("Сервер запущен", flush=True)
                k += 1

            elif k > 1:
                pass

            time.sleep(1)
    except Exception as e:
        print(f'Error: {e}')
    finally:
        print("заканчиваю работу")
