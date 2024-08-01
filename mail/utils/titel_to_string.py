from email.header import decode_header


def decode_mime_words(s):  # функция превращает заголовки  email  в более читаемую версию
    decoded_string = ''
    for word, encoding in decode_header(s):
        if isinstance(word, bytes):
            decoded_string += word.decode(encoding if encoding else 'utf-8')
        else:
            decoded_string += word
    return decoded_string
