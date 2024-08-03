import re


def url_to_id(url):
    # Регулярное выражение для извлечения ID из ссылки Notion
    pattern = re.compile(r'https://www\.notion\.so/.*?([a-f0-9]{32})')
    match = pattern.search(url)
    if match:
        return match.group(1)
    else:
        return None
