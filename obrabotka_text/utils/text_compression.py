from textwrap import shorten


def compress_text(text, max_length=2000):
    """
    Сжимает текст до максимальной длины, сохраняя смысл и структуру.

    :param text: Исходный текст
    :param max_length: Максимальная длина текста
    :return: Сжатый текст
    """
    if len(text) <= max_length:
        return text

    # Используем функцию shorten для обрезкиq текста до нужной длины с сохранением структуры
    # Убедимся, что мы не обрезаем слова
    compressed_text = shorten(text, width=max_length, placeholder="...")

    return compressed_text
