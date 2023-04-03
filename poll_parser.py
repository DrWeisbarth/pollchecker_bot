def message_to_list(message: str) -> list:
    return [string.strip() for string in message.split("\n")]


def list_to_message(_list: list) -> str:
    message = "Liste Ihrer Strings:\n\n"
    for l in _list:
        message = message + l + "\n"
    return message
