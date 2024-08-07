import re


def extract_text_between_timestamps(text):
    # Регулярное выражение для поиска меток времени и текста между ними
    pattern = re.compile(r'\d{2}:\d{2}\s*(.*?)(?=\d{2}:\d{2}|$)', re.DOTALL)
    matches = pattern.findall(text)

    # Очистка и удаление лишних символов новой строки
    cleaned_matches = [re.sub(r'\s+', ' ', match).strip() for match in matches]

    return cleaned_matches