import email
import time
from utils.titel_to_string import decode_mime_words
from utils.body_email_to_string import extract_text_from_html
import imaplib

# Почтовые данные
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = 'arttdydnik@gmail.com'
PASSWORD = 'fyax omnj uobc fwve'


def connect_to_mail_server():
    """Подключение к почтовому серверу и аутентификация."""
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.select('inbox')
    return mail


def fetch_unseen_emails(mail):
    """Поиск непрочитанных писем и возвращение их ID."""
    status, messages = mail.search(None, '(UNSEEN)')
    return messages[0].split()


def process_email(mail_id, mail):
    """Обработка отдельного письма по его ID."""
    status, msg_data = mail.fetch(mail_id, '(RFC822)')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject = decode_header_field(msg['Subject'])
            from_ = decode_header_field(msg['From'])
            print('Subject:', subject)
            print('From:', from_)
            body = extract_body_from_message(msg)
            if body:
                print('Body:', body)
            else:
                print('No text/plain or text/html body found')


def decode_header_field(header):
    """Декодирование заголовка с поддержкой MIME."""
    if header:
        return decode_mime_words(header)
    return '(No Subject)' if header == 'Subject' else '(Unknown Sender)'


def extract_body_from_message(msg):
    """Извлечение тела письма из сообщения."""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition'))
            try:
                part_body = part.get_payload(decode=True).decode()
            except:
                part_body = '(Unable to decode body)'
            if content_type == 'text/plain' and 'attachment' not in content_disposition:
                return part_body
            elif content_type == 'text/html' and 'attachment' not in content_disposition:
                return extract_text_from_html(part_body)
    else:
        content_type = msg.get_content_type()
        try:
            body = msg.get_payload(decode=True).decode()
        except:
            body = '(Unable to decode body)'
        if content_type == 'text/html':
            return extract_text_from_html(body)
        return body
    return None


def close_connection(mail):
    """Закрытие соединения с почтовым сервером."""
    mail.close()
    mail.logout()


def check_mail():
    """Основная функция для проверки почты."""
    try:
        mail = connect_to_mail_server()
        mail_ids = fetch_unseen_emails(mail)
        for mail_id in mail_ids:
            process_email(mail_id, mail)
        close_connection(mail)
    except Exception as e:
        print(f'Error: {e}')


# Запуск функции проверки почты
if __name__ == '__main__':
    print("Запуск сервера")
    while True:
        check_mail()
        time.sleep(1)
