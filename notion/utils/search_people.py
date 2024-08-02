import requests

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