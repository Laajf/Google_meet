from ..utils.connect_and_find_mails import connect_to_mail_server, fetch_unseen_emails
from ..utils.treatment_mail import process_email, close_connection

# Почтовые данные
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = 'arttdydnik@gmail.com'
PASSWORD = 'fyax omnj uobc fwve'


def check_mail():
    """Основная функция для проверки почты."""
    try:
        mail = connect_to_mail_server(IMAP_SERVER, EMAIL_ACCOUNT, PASSWORD)
        mail_ids = fetch_unseen_emails(mail)
        for mail_id in mail_ids:
            process_email(mail_id, mail)
        close_connection(mail)
    except Exception as e:
        print(f'Error: {e}')
