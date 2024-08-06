from .titel_to_string import decode_mime_words
from .body_email_to_string import extract_text_from_html
import email

from_ = ""


def process_email(mail_id, mail):
    """Обработка отдельного письма по его ID."""
    global from_
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
                return body
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
