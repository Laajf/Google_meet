import re


def string_to_email(string):
    # Регулярное выражение для извлечения email
    match = re.search(r'<(.*?)>', string)

    if match:
        email = match.group(1)
        print(f"""




{email}




""")
        return email
    else:
        return "Email не найден"
