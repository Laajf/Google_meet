import email
import time
from utils.titel_to_string import decode_mime_words
from utils.body_email_to_string import extract_text_from_html
import imaplib


# Почтовые данные
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = 'arttdydnik@gmail.com'
PASSWORD = 'fyax omnj uobc fwve'


def check_mail():
    try:

        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, PASSWORD)
        mail.select('inbox')

        # Поиск непрочитанных писем
        status, messages = mail.search(None, '(UNSEEN)')

        mail_ids = messages[0].split()
        for mail_id in mail_ids:
            status, msg_data = mail.fetch(mail_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    # Обработка заголовка Subject
                    subject_header = msg['Subject']
                    if subject_header:
                        subject = decode_mime_words(subject_header)
                    else:
                        subject = '(No Subject)'

                    # Обработка заголовка From
                    from_header = msg['From']
                    if from_header:
                        from_ = decode_mime_words(from_header)
                    else:
                        from_ = '(Unknown Sender)'

                    print('Subject:', subject)
                    print('From:', from_)

                    # Инициализация переменной для хранения тела письма
                    body = None

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get('Content-Disposition'))

                            try:
                                part_body = part.get_payload(decode=True).decode()
                            except:
                                part_body = '(Unable to decode body)'

                            if content_type == 'text/plain' and 'attachment' not in content_disposition:
                                body = part_body
                                break  # Остановиться после нахождения текстовой части
                            elif content_type == 'text/html' and 'attachment' not in content_disposition:
                                # Извлечь текст из HTML
                                body = extract_text_from_html(part_body)
                                break  # Остановиться после нахождения HTML части
                    else:
                        content_type = msg.get_content_type()
                        try:
                            body = msg.get_payload(decode=True).decode()
                        except:
                            body = '(Unable to decode body)'
                        if content_type == 'text/html':
                            # Извлечь текст из HTML
                            body = extract_text_from_html(body)

                    if body:
                        print('Body:', body)
                    else:
                        print('No text/plain or text/html body found')

        mail.close()
        mail.logout()
    except Exception as e:
        print(f'Error: {e}')


if __name__ == "__main__":
    print("Запуск проверки почты")
    while True:
        check_mail()
        time.sleep(1)  # Проверять почту каждые 60 секунд
