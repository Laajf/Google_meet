import re


def clean_text(text):
    # Определяем шаблоны для удаления
    if text is not None:
        patterns = [
            # Удаление информации о встрече и датах
            r'Instant meeting notes.*?with you\.',
            r'Date:.*?\d{1,2} [a-zA-Z]+ \d{4}, \d{2}:\d{2}- \d{2}:\d{2} GMT[+-]\d{2}:\d{2}',

            # Удаление информации о платформе MeetGeek
            r'MeetGeek is the meeting automation platform.*?Update your email preferences\.',

            # Общие шаблоны для MeetGeek
            r'MeetGeek Virtual Meeting Assistant \| MeetGeek',
            r'MeetGeek AI \| Your Virtual Meeting Assistant',
            r'Diamore Notetaker shared',

            # Удаление блока с информацией о встрече
            r'Attendees:.*?Meeting Summary',
        ]

        # Применяем шаблоны для удаления соответствующих текстов
        for pattern in patterns:
            text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)

        # Убираем лишние пробелы и переносы строк
        text = re.sub(r'\s+', ' ', text).strip()

        return text
    else:
        return None
