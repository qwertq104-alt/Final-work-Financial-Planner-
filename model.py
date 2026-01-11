# model.py
import pandas as pd
import os
from validation import clean_category, clean_comment  # Модули для очистки данных

class FinancialModel:
    def __init__(self, csv_file):
        """
        Инициализирует модель данных.
        :param csv_file: Путь к файлу .csv.
        """
        self.csv_file = csv_file
        self.load_data()

    def load_data(self):
        """
        Загружает данные из файла .csv.
        Если файл не существует, создаётся пустой DataFrame.
        """
        directory = os.path.dirname(self.csv_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        try:
            self.data = pd.read_csv(self.csv_file)
        except FileNotFoundError:
            columns = ["Amount", "Transaction_Type", "Date", "Category", "Comment"]
            self.data = pd.DataFrame(columns=columns)

    def get_data(self):
        """
        Возвращает копию данных.
        """
        return self.data.copy()

    def save_data(self):
        """
        Сохраняет данные в файл .csv.
        """
        self.data.to_csv(self.csv_file, index=False)

    def add_transaction(self, amount, transaction_type, date, category, comment):
        """
        Добавляет новую транзакцию.
        """
        new_row = pd.DataFrame({
            "Amount": [amount],
            "Transaction_Type": [transaction_type],
            "Date": [date],
            "Category": [category],
            "Comment": [comment]
        })
        self.data = pd.concat([self.data, new_row], ignore_index=True)

    def delete_transaction(self, index):
        """
        Удаляет транзакцию по индексу.
        """
        self.data.drop(index, inplace=True)

    def filter_by_category(self, category):
        """
        Фильтрует транзакции по категории.
        """
        return self.data[self.data["Category"].str.lower() == category.lower()]

    def calculate_balance(self):
        """
        Вычисляет текущий баланс.
        """
        income = self.data.query("Transaction_Type == 'Income'")["Amount"].sum()
        expenses = self.data.query("Transaction_Type == 'Expense'")["Amount"].sum()
        return income - expenses

    def clean_data(self, data=None):
        """
        Очищает данные, удаляя специальные символы из категорий и комментариев.
        """
        if data is None:
            data = self.data
        cleaned_data = data.copy()
        cleaned_data["Category"] = cleaned_data["Category"].apply(clean_category)
        cleaned_data["Comment"] = cleaned_data["Comment"].apply(clean_comment)
        return cleaned_data

    def reset_data(self):
        """
        Сбрасывает все данные, формируя пустую таблицу.
        """
        columns = ["Amount", "Transaction_Type", "Date", "Category", "Comment"]
        self.data = pd.DataFrame(columns=columns)

    def save_changes(self):
        """
        Сохраняет изменения в файл.
        """
        self.data.to_csv(self.csv_file, index=False)