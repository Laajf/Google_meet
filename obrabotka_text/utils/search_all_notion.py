import requests
def search_notion(secret_key, query, page_size=100):
    url = "https://api.notion.com/v1/search"

    payload = {
        "query": query,
        #"page_size": page_size
    }

    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": f"Bearer {secret_key}"
    }

    response = requests.post(url, json=payload, headers=headers)

    # Распечатываем полный ответ для отладки
    print("API Response:", response.json())

    # Проверяем, есть ли ключ 'results'
    response_data = response.json()
    if 'results' not in response_data:
        raise KeyError("Ключ 'results' не найден в ответе API Notion.")

    return response_data