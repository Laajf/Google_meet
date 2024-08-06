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
from obrabotka_text.utils.obrezka_text import clean_text


def run_mail():
    k = 0
    print("Запуск сервера", flush=True)
    try:
        while True:
            body = check_mail()
            body_save = body
            body_save = clean_text(body_save)
            if body_save is not None:
                # print(body)
                secret_key = get_config_value('secret_key')

                url = main(secret_key=secret_key, meetgeek_transcript=body)
                page_id = url_to_id(url)
                body_save = compress_text(body_save)

                # print(f"{treatment_mail.from_}")
                string_email = string_to_email(treatment_mail.from_)
                if string_email == "app@meetgeek.ai":
                    create_comment(page_id, body_save)
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
