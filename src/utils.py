import json
from datetime import datetime


def operations_file(filename):
    """
    Возвращает файл json с
    данными по банковским операциям.
    """
    with open(filename, encoding='utf-8') as file:
        operations = json.load(file)
        return operations


def get_date(operations):
    """Возращает значение с датой по ключу."""
    return operations['date']


def last_operations(operations):
    """
    Выбирает выполненные операции, сортирует
    их по дате и возвращает список 5-ти последних операций.
    """
    executed_operations = [op for op in operations if op.get('state') == 'EXECUTED']
    sorted_operations = sorted(executed_operations, key=get_date, reverse=True)
    five_last_operations = sorted_operations[:5]
    return five_last_operations


def mask_card_number(card_number):
    """
    Возвращает замаскированные номера счетов
    и карт отправителя если они есть.
    """
    if 'Счет' in card_number:
        masked_number = card_number[:5] + '**' + card_number[-4:]
        return masked_number
    elif 'Unknown' in card_number:
        return 'Unknown'
    else:
        masked_number = card_number[:-16] + card_number[-16:-12] + ' ' + \
                        card_number[-12:-10] + '** **** ' + card_number[-4:]
        return masked_number


def mask_account_number(account_number):
    """Возвращает замаскированные номера счетов получателя."""
    masked_number = account_number[:5] + '**' + account_number[-4:]
    return masked_number


def print_last_operations(file_last_operations):
    """
    Выводит пользователю 5 последних
    операций в определенном формате.
    """
    for operation in file_last_operations:
        # Вытягиваем строку с датой, переводим ее в объект
        # даты и затем форматируем в нужный вид ДД.ММ.ГГГГ.
        date_str = operation['date'][:10]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        date = date_obj.strftime("%d.%m.%Y")

        # Описание банковской операции.
        description = operation['description']

        # Номер "от" кого перевод (если он виден) и
        # номер "кому" перевод
        from_card = operation.get('from', 'Unknown')
        to_card = operation['to']

        # Сумма и валюта перевода.
        amount = operation['operationAmount']['amount']
        currency = operation['operationAmount']['currency']['name']

        # Вызов функций маскирующих номера счетов/карт.
        masked_from = mask_card_number(from_card)
        masked_to = mask_account_number(to_card)

        # Вывод информации в нужном формате.
        print(f'''{date} {description}
{masked_from} -> {masked_to}
{amount} {currency}\n''')
