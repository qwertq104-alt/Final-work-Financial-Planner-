#controller.py
from model import FinancialModel  # Подключение модуля с финансовым модулем

# Контроллер финансов - управляет основными действиями над финансовыми данными
class FinancialController:
    def __init__(self, csv_file):  # Конструктор принимает путь к файлу CSV
        self.model = FinancialModel(csv_file)  # Инициализируем финансовый модуль с указанным файлом

    # Метод добавления новой финансовой операции
    def add_transaction(self, *args):
        # args содержит все аргументы, передаваемые в метод (сумма, тип, дата и т.п.)
        self.model.add_transaction(*args)  # Добавляем транзакцию в модель
        self.model.save_data()  # Сохраняем обновленные данные обратно в файл

    # Метод удаления существующей транзакции по её индексу
    def delete_transaction(self, index):
        self.model.delete_transaction(index)  # Удаляем транзакцию по переданному индексу
        self.model.save_data()  # Обновляем файл данных

    # Метод фильтрации транзакций по выбранной категории
    def filter_by_category(self, category):
        return self.model.filter_by_category(category)  # Возвращаем отфильтрованные транзакции

    # Метод фильтрации транзакций по временному промежутку
    def filter_by_date(self, start_date, end_date):
        return self.model.filter_by_date(start_date, end_date)  # Возвращаем транзакции за выбранный диапазон дат

    # Метод вычисления текущего финансового баланса
    def calculate_balance(self):
        return self.model.calculate_balance()  # Возврат общего баланса (разницы между доходами и расходами)