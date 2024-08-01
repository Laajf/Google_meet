import requests
from sentence_transformers import SentenceTransformer, util
#from notion
# Загрузка модели для извлечения признаков
model = SentenceTransformer('all-Mpnet-base-v2')


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


def find_most_similar_notion_page(combined_text, notion_pages, similarity_threshold=0.1):
    # Создание векторного представления текста
    text_embedding = model.encode(combined_text, convert_to_tensor=True)

    max_similarity = 0
    best_page = None

    for page in notion_pages:
        # Используем заголовок и контент страницы для улучшения поиска
        page_title = page['properties']['title']['title'][0]['plain_text']
        page_content = page.get('properties', {}).get('content', {}).get('rich_text', [{}])
        page_content_text = ' '.join([r.get('text', {}).get('content', '') for r in page_content])

        page_text = f"{page_title} {page_content_text}"
        page_embedding = model.encode(page_text, convert_to_tensor=True)

        # Вычисление сходства
        similarity_score = util.pytorch_cos_sim(text_embedding, page_embedding).item()

        if similarity_score > max_similarity:
            max_similarity = similarity_score
            best_page = page

    if max_similarity >= similarity_threshold:
        return best_page
    else:
        return None


def analyze_meetgeek_transcript(transcript):
    # Разбиваем текст на сегменты по времени
    segments = transcript.split('\n\n')

    # Объединяем все сегменты в один текст
    combined_text = ' '.join(segment.strip() for segment in segments if segment.strip())

    return combined_text


def main(secret_key, meetgeek_transcript):
    # Шаг 1: Анализ выгрузки из MeetGeek
    combined_text = analyze_meetgeek_transcript(meetgeek_transcript)

    # Шаг 2: Поиск страниц в Notion
    notion_data = search_notion(secret_key, "")

    # Обработка ответа от API
    notion_pages = notion_data.get('results', [])

    if not notion_pages:
        print("Не удалось найти страницы в Notion.")
        return

    # Шаг 3: Поиск наиболее похожей страницы
    similar_page = find_most_similar_notion_page(combined_text, notion_pages)

    if similar_page:
        print(f"Текст из MeetGeek:\n{combined_text}\n")
        print(f"Наиболее похожая страница в Notion:\n{similar_page['properties']['title']['title'][0]['plain_text']}\n")
        print(f"URL: {similar_page['url']}\n")
        return similar_page['url']
    else:
        print("Нет подходящей страницы в Notion.")


# Пример использования
if __name__ == "__main__":
    secret_key = "secret_Ru3ArATfhvqadwy8KGZWPcJgKVDocWDIL8xvGrjt8Gh"
    meetgeek_transcript = """
    00:00

    NOTION API хороший инструмент для работы    
    ...

    30:52

    Meeting ended
    """
    main(secret_key, meetgeek_transcript)
