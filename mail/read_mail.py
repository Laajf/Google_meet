import imaplib
import email
from email.header import decode_header
import time

# Почтовые данные
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = 'arttdydnik@gmail.com'
PASSWORD = 'fyax omnj uobc fwve'


def decode_mime_words(s):
    decoded_string = ''
    for word, encoding in decode_header(s):
        if isinstance(word, bytes):
            decoded_string += word.decode(encoding if encoding else 'utf-8')
        else:
            decoded_string += word
    return decoded_string


def check_mail():
    try:
        # Подключение к серверу
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
                    else:
                        content_type = msg.get_content_type()
                        try:
                            body = msg.get_payload(decode=True).decode()
                        except:
                            body = '(Unable to decode body)'

                    if body:
                        print('Body:', body)
                    else:
                        print('No text/plain body found')

        mail.close()
        mail.logout()
    except Exception as e:
        print(f'Error: {e}')




if __name__ == "__main__":
    while True:
        check_mail()
        time.sleep(1)  # Проверять почту каждые 60 секунд
