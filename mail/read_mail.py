import time
# from service.service import check_mail
from mail.service.service import check_mail
from obrabotka_text.service.service import main
from obrabotka_text.utils.url_to_page_id import url_to_id
from notion.utils.create_comment import create_comment
from obrabotka_text.utils.text_compression import compress_text
from for_user.utils.json_to_variable import get_config_value


def run_mail():
    print("Запуск сервера", flush=True)
    try:
        while True:
            body = check_mail()
            body_save = body
            if body is not None:
                print(body)
                secret_key = get_config_value('secret_key')

                url = main(secret_key=secret_key, meetgeek_transcript=body)
                page_id = url_to_id(url)
                body_save = compress_text(body_save)
                create_comment(page_id, body_save)
            time.sleep(1)
    except Exception as e:
        print(f'Error: {e}')
    finally:
        print("заканчиваю работу")
