from obrabotka_text.utils.search_all_notion import search_notion
from obrabotka_text.utils.text_analysis import analyze_meetgeek_transcript, find_most_similar_notion_page


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
