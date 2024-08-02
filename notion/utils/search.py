import requests

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

