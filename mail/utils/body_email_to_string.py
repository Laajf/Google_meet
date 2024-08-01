from bs4 import BeautifulSoup


def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Замена тегов <br> и <p> на новые строки для лучшего форматирования
    for br in soup.find_all('br'):
        br.replace_with('\n')
    for p in soup.find_all('p'):
        p.insert_before('\n')
        p.insert_after('\n')

    text = soup.get_text(separator='\n', strip=True)
    return text
