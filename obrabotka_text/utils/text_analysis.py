from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-Mpnet-base-v2')


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
