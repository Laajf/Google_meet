import requests
from transformers import AutoTokenizer, AutoModel
import torch
import sys
import io

# Установка кодировки вывода
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Загрузка модели для извлечения признаков
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")


def search_notion(secret_key, query, page_size=100):
    url = "https://api.notion.com/v1/search"

    payload = {
        "query": query,
        "page_size": page_size
    }

    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": f"Bearer {secret_key}"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def get_text_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings


def cosine_similarity_tensor(a, b):
    dot_product = torch.matmul(a, b.T)
    norm_a = a.norm(dim=1).unsqueeze(1)
    norm_b = b.norm(dim=1).unsqueeze(0)
    return dot_product / (norm_a * norm_b)


def find_most_similar_notion_page(combined_text, notion_pages, similarity_threshold=0.2):
    text_embedding = get_text_embedding(combined_text)

    max_similarity = 0
    best_page = None

    for page in notion_pages:
        # Используем заголовок и контент страницы для улучшения поиска
        page_title = page['properties']['title']['title'][0]['plain_text']
        page_content = page.get('properties', {}).get('content', {}).get('rich_text', [{}])
        page_content_text = ' '.join([r.get('text', {}).get('content', '') for r in page_content])

        page_text = f"{page_title} {page_content_text}"
        page_embedding = get_text_embedding(page_text)
        similarity_score = cosine_similarity_tensor(text_embedding, page_embedding).item()

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
    notion_pages = notion_data['results']

    # Шаг 3: Поиск наиболее похожей страницы
    similar_page = find_most_similar_notion_page(combined_text, notion_pages)

    if similar_page:
        print(f"Текст из MeetGeek:\n{combined_text}\n")
        print(f"Наиболее похожая страница в Notion:\n{similar_page['properties']['title']['title'][0]['plain_text']}\n")
        print(f"URL: {similar_page['url']}\n")
    else:
        print("Нет подходящей страницы в Notion.")


# Пример использования
if __name__ == "__main__":
    secret_key = "secret_Ru3ArATfhvqadwy8KGZWPcJgKVDocWDIL8xvGrjt8Gh"
    meetgeek_transcript = """
    00:00

    google meet неплохой сервис для работы с звонками
    ...

    30:52

    Meeting ended
    """
    main(secret_key, meetgeek_transcript)
