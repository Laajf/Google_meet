import requests


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
