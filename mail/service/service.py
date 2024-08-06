from ..utils.connect_and_find_mails import connect_to_mail_server, fetch_unseen_emails
from ..utils.treatment_mail import process_email, close_connection
from for_user.utils.json_to_variable import get_config_value
# Почтовые данные
IMAP_SERVER = get_config_value("IMAP_SERVER")
EMAIL_ACCOUNT = get_config_value("EMAIL_ACCOUNT")
PASSWORD = get_config_value("PASSWORD")


def check_mail():
    """Основная функция для проверки почты."""
    global body
    try:
        body = None
        mail = connect_to_mail_server(IMAP_SERVER, EMAIL_ACCOUNT, PASSWORD)
        mail_ids = fetch_unseen_emails(mail)
        for mail_id in mail_ids:
            body = process_email(mail_id, mail)
        close_connection(mail)
        if body is None:
            pass
        else:
            return body
    except Exception as e:
        print(f'Error: {e}')
