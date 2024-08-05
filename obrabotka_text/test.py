from service.service import main
from for_user.utils.json_to_variable import get_config_value

# Пример использования
if __name__ == "__main__":
    secret_key = get_config_value("secret_key")
    meetgeek_transcript = """
    00:00

    NOTION API хороший инструмент для работы    
    ...

    30:52

    Meeting ended
    """
    main(secret_key, meetgeek_transcript)
