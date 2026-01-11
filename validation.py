# validation.py
import re
import datetime

# Регулярные выражения для проверки данных
RE_AMOUNT = r"^[+-]?\d+(\.\d+)?$"     # Цифровая сумма (может содержать точку)
RE_DATE = r"\d{4}-\d{2}-\d{2}"        # Дата в формате YYYY-MM-DD
RE_CATEGORY = r"^[a-zA-Zа-яА-ЯёЁ\s]+$"# Категория (буквы и пробелы)
RE_COMMENT = r"^.{0,100}$"            # Комментарий длиной максимум 100 символов

# Шаблоны очистки данных
RE_CLEAN_CATEGORY = r"[^\w\s]"         # Специальные символы в категориях
RE_CLEAN_COMMENT = r"[^\w\s.,?!]"     # Спецсимволы в комментариях

# Валидаторы полей
def validate_amount(amount):
    """Проверяет корректность суммы."""
    return bool(re.match(RE_AMOUNT, str(amount)))

def validate_date(date_str):
    """Проверяет формат даты."""
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_category(category):
    """Проверяет формат категории."""
    return bool(re.match(RE_CATEGORY, category))

def validate_comment(comment):
    """Проверяет длину комментария."""
    return bool(re.match(RE_COMMENT, comment))

# Функции очистки данных
def clean_category(category):
    """Очищает категорию от спецсимволов."""
    cleaned = re.sub(RE_CLEAN_CATEGORY, '', category.strip())
    return cleaned.strip()

def clean_comment(comment):
    """Очищает комментарий от спецсимволов."""
    cleaned = re.sub(RE_CLEAN_COMMENT, '', comment)
    return cleaned.strip()

# Главная функция проверки транзакции
def validate_transaction(amount, type_, date, category, comment):
    errors = []

    # Проверка суммы
    if not validate_amount(amount):
        errors.append("Некорректная сумма")

    # Проверка типа транзакции
    if type_.lower() not in ['income', 'expense']:
        errors.append("Тип транзакции должен быть Income или Expense")

    # Проверка даты
    if not validate_date(date):
        errors.append("Некорректная дата, используйте формат YYYY-MM-DD")

    # Проверка категории
    if not validate_category(category):
        errors.append("Некорректная категория, только буквы и пробелы разрешены")

    # Проверка комментария
    if not validate_comment(comment):
        errors.append("Комментарий слишком длинный (более 100 символов)")

    return errors