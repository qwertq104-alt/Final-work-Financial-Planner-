#business_logic.py
from analytics import Analytics, Visualization

# Бизнес-логика приложения
class BusinessLogic:
    def __init__(self, model):
        # Модель данных
        self.model = model

    def calculate_balance(self):
        """
        Подсчитывает текущий баланс.
        """
        income = self.model.data.query("Transaction_Type == 'Income'").Amount.sum()
        expenses = self.model.data.query("Transaction_Type == 'Expense'").Amount.sum()
        return income - expenses

    def add_transaction(self, amount, type_, date, category, comment=''):
        """
        Добавляет новую транзакцию.
        """
        self.model.add_transaction(amount, type_, date, category, comment)
        self.model.save_changes()

    def delete_transaction(self, index):
        """
        Удаляет транзакцию по индексу.
        """
        self.model.delete_transaction(index)


# Менеджер транзакций
class TransactionManager:
    def __init__(self, controller):
        # Контроллер для взаимодействия с моделью
        self.controller = controller
        # Аналитика для отчетности
        self.analytics = Analytics(controller.model.data)
        # Визуализация для графики
        self.visualization = Visualization(controller.model.data)

    def add_transaction(self, amount, transaction_type, date, category, comment=""):
        """
        Добавляет новую финансовую операцию.
        """
        self.controller.add_transaction(amount, transaction_type, date, category, comment)

    def delete_transaction(self, index):
        """
        Удаляет транзакцию по её индексу.
        """
        self.controller.delete_transaction(index)

    def filter_by_category(self, category):
        """
        Возвращает транзакции заданной категории.
        """
        return self.analytics.filter_by_category(category)

    def get_all_transactions(self):
        """
        Возвращает все доступные транзакции.
        """
        return self.controller.model.data.copy()

    def calculate_balance(self):
        """
        Вычисляет баланс счетов.
        """
        return self.controller.calculate_balance()

    def analyze_categories(self):
        """
        Отчеты по расходам по категориям.
        """
        return self.analytics.analyze_categories()

    def analyze_period(self, start_date, end_date):
        """
        Анализ бюджета за указанный период.
        """
        return self.analytics.analyze_period(start_date, end_date)

    def get_top_expenses(self, n=5):
        """
        Список самых крупных расходов.
        """
        return self.analytics.get_top_expenses(n)

    def plot_income_vs_expenses_over_time(self):
        """
        График динамики доходов и расходов.
        """
        self.visualization.plot_income_vs_expenses_over_time()

    def plot_pie_chart_categories(self):
        """
        Круговая диаграмма расходов по категориям.
        """
        self.visualization.plot_pie_chart_categories()

    def plot_bar_chart_top_expenses(self, n=5):
        """
        Гистограмма топовых расходов.
        """
        self.visualization.plot_bar_chart_top_expenses(n)