import requests
import json
from for_user.utils.json_to_variable import get_config_value

def create_comment(PAGE_ID, text):
    # URL для создания комментария
    url = "https://api.notion.com/v1/comments"  # Замените на актуальный эндпоинт


    secret_key = get_config_value("secret_key")

    # Заголовки запроса
    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": f"Bearer {secret_key}"
        # Замените на ваш новый секретный токен
    }

    # Тело запроса с данными комментария
    payload = {
        "parent": {
            "page_id": f"{PAGE_ID}"  # Замените на идентификатор вашей страницы
        },
        "rich_text": [  # Убедитесь, что поле rich_text определено
            {
                "type": "text",
                "text": {
                    "content": f"{text}"  # Содержание комментария
                }
            }
        ]
    }

    # Выполнение POST запроса
    response = requests.post(url, json=payload, headers=headers)

    # Проверка статуса ответа и печать результата
    if response.status_code == 200:
        response_data = response.json()
        print("Комментарий создан:", json.dumps(response_data, ensure_ascii=False, indent=4))
    else:
        print(f"Ошибка: {response.status_code}")
        print(response.text)
        if response.status_code == 401:
            print("Ошибка авторизации: проверьте секретный токен.")
        elif response.status_code == 403:
            print("Доступ запрещен: проверьте права доступа.")
        else:
            print("Произошла другая ошибка.")
