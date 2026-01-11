# analytics.py
import matplotlib.pyplot as plt  # Библиотека для построения графиков

# Базовые характеристики данных
def analyze_data(data):
    """
    Подсчитывает количество элементов, среднее и максимальное значение.
    """
    return len(data), data.mean(), data.max()

# Основной класс для анализа финансовых данных
class Analytics:
    def __init__(self, df):
        # Копируем данные, чтобы обезопасить исходный DataFrame
        self.df = df.copy()

    def filter_by_category(self, category):
        """
        Фильтрует данные по категории, игнорируя регистр.
        """
        filtered_df = self.df[self.df['Category'].str.lower() == category.lower()]
        return filtered_df

    def analyze_categories(self):
        """
        Суммирует расходы по каждой категории.
        """
        expenses = self.df.query("Transaction_Type == 'Expense'")
        result = expenses.groupby("Category")["Amount"].sum()
        return result

    def analyze_period(self, start_date, end_date):
        """
        Анализирует доходы и расходы за указанный период.
        """
        period_df = self.df[(self.df["Date"] >= start_date) & (self.df["Date"] <= end_date)]
        income = period_df.query("Transaction_Type == 'Income'")["Amount"].sum()
        expenses = period_df.query("Transaction_Type == 'Expense'")["Amount"].sum()
        return income, expenses

    def get_top_expenses(self, n=5):
        """
        Возвращает список самых крупных расходов.
        """
        expenses = self.df.query("Transaction_Type == 'Expense'")
        sorted_expenses = expenses.nlargest(n, "Amount")
        return sorted_expenses

# Класс для визуализации данных
class Visualization:
    def __init__(self, df):
        # Создаем экземпляр класса аналитики
        self.analytics = Analytics(df)

    def plot_income_vs_expenses_over_time(self):
        """
        Линейный график доходов и расходов за первые три дня.
        """
        grouped = self.analytics.df.groupby(['Date', 'Transaction_Type'])['Amount'].sum().unstack(fill_value=0)
        unique_dates = sorted(grouped.index.unique())[:3]
        first_three_days_grouped = grouped.loc[unique_dates]
        first_three_days_grouped.plot(kind="line", title="Доходы и расходы за первые три дня")
        plt.xlabel("Дата")
        plt.ylabel("Сумма")
        plt.legend(["Доходы", "Расходы"])
        plt.show()

    def plot_pie_chart_categories(self):
        """
        Круговая диаграмма расходов по категориям.
        """
        expenses = self.analytics.analyze_categories()
        plt.figure(figsize=(8, 8))
        plt.pie(expenses.values, labels=expenses.index.str.capitalize(), autopct="%1.1f%%")
        plt.title("Расходы по категориям")
        plt.show()

    def plot_bar_chart_top_expenses(self, n=5):
        """
        Гистограмма самых крупных расходов.
        """
        top_expenses = self.analytics.get_top_expenses(n)
        plt.figure(figsize=(10, 6))
        plt.bar(top_expenses["Category"].str.capitalize(), top_expenses["Amount"])
        plt.xlabel("Категория")
        plt.ylabel("Сумма")
        plt.title(f"Топ {n} крупные расходы")
        plt.xticks(rotation=45)
        plt.show()