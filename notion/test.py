import requests
import json

secret_key_notion = "secret_Ru3ArATfhvqadwy8KGZWPcJgKVDocWDIL8xvGrjt8Gh"


def search_people(secret_key):
    url = "https://api.notion.com/v1/users"

    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": f"Bearer {secret_key}"
    }

    response = requests.get(url, headers=headers)
    print(response.status_code)
    print(response.text)


def get_page(secret_key, page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": f"Bearer {secret_key}"
    }

    response = requests.get(url, headers=headers)

    print(response.status_code)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.json()}")


def search(secret_key):
    url = "https://api.notion.com/v1/search"

    # Параметры запроса
    payload = {
        # "query": "собака",  # Ваша строка запроса
        # "sort": {
        #   "direction": "ascending",  # Направление сортировки (ascending или descending)
        #  "timestamp": "last_edited_time"  # Поле для сортировки (last_edited_time или created_time)
        # },
        # "filter": {
        #   "value": "page",  # Фильтр по типу (page, database и т.д.)
        #  "property": "object"  # Поле для фильтрации (object, title и т.д.)
        # },
        "page_size": 10000000000  # Размер страницы (максимум 100)
    }

    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": f"Bearer {secret_key}"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.json())


def create_comment(PAGE_ID):
    # URL для создания комментария
    url = "https://api.notion.com/v1/comments"  # Замените на актуальный эндпоинт

    # Заголовки запроса
    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": "Bearer secret_Ru3ArATfhvqadwy8KGZWPcJgKVDocWDIL8xvGrjt8Gh"  # Замените на ваш новый секретный токен
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
                    "content": "тест комментария"  # Содержание комментария
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


create_comment("97efc5598c94477d8f3512a3f761f10f")
