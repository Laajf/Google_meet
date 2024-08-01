import imaplib
def connect_to_mail_server(IMAP_SERVER, EMAIL_ACCOUNT, PASSWORD):
    """Подключение к почтовому серверу и аутентификация."""
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.select('inbox')
    return mail


def fetch_unseen_emails(mail):
    """Поиск непрочитанных писем и возвращение их ID."""
    status, messages = mail.search(None, '(UNSEEN)')
    return messages[0].split()