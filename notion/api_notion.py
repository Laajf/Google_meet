import os
from notion_client import Client

# Убедись, что ты используешь правильный токен
notion_token = "secret_b52kb92DdHd3PwirGSBI5t7MgkSPFhDXn4oYrMnFdb2"
database_id = "e088481b0401411499007def8d852bbb"

# Инициализация клиента
notion = Client(auth=notion_token)

try:
    # Получение данных из базы данных
    response = notion.databases.query(database_id=database_id)

    # Вывод данных
    for result in response['results']:
        print(result['properties'])
except Exception as e:
    print(f"An error occurred: {e}")
