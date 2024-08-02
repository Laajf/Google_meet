from service.service import main


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
