# view_tkinter.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import date
from validation import validate_transaction
from test_suite import run_all_tests

# Главный класс приложения
class FinancialApp(tk.Tk):
    def __init__(self, logic_manager):
        super().__init__()
        self.logic_manager = logic_manager
        self.title("Финансовый планер")
        self.geometry("1000x700")

        # Интерфейс
        self.create_menu()
        self.create_transaction_form()
        self.create_filter_section()
        self.create_transactions_list()
        self.create_balance_display()

        # Заполнение таблицы транзакций
        self.update_transactions_list()

    def create_menu(self):
        """Меню приложения"""
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        # Меню операций
        operations_menu = tk.Menu(menu_bar, tearoff=0)
        operations_menu.add_separator()
        operations_menu.add_command(label="Выход", command=self.quit)
        menu_bar.add_cascade(label="Операции", menu=operations_menu)

        # Меню аналитики
        analytics_menu = tk.Menu(menu_bar, tearoff=0)
        analytics_menu.add_command(label="Доходы/расходы", command=self.plot_income_vs_expenses)
        analytics_menu.add_command(label="Категории", command=self.plot_pie_chart_categories)
        analytics_menu.add_command(label="Крупные траты", command=self.plot_top_expenses)
        menu_bar.add_cascade(label="Аналитика", menu=analytics_menu)

        # Меню тестов
        tests_menu = tk.Menu(menu_bar, tearoff=0)
        tests_menu.add_command(label="Запустить тесты", command=self.run_tests)
        menu_bar.add_cascade(label="Тесты", menu=tests_menu)

    def run_tests(self):
        """Запуск тестов и вывод отчёта"""
        total_tests, success_count, failures, errors = run_all_tests()
        report = f"Тестов выполнено: {total_tests}\nПрошло успешно: {success_count}\nПровалилось: {failures}\nОшибок: {errors}"
        messagebox.showinfo("Тесты завершились", report)

    def create_transaction_form(self):
        """Форма для добавления транзакций"""
        frame = ttk.Labelframe(self, text="Новая транзакция")
        frame.pack(fill="both", expand="yes", padx=10, pady=10)

        # Выбор типа операции
        ttk.Label(frame, text="Тип:").grid(row=0, column=0, sticky="w")
        self.transaction_type_var = tk.StringVar(value="Income")
        ttk.Radiobutton(frame, text="Доход", variable=self.transaction_type_var, value="Income").grid(row=0, column=1)
        ttk.Radiobutton(frame, text="Расход", variable=self.transaction_type_var, value="Expense").grid(row=0, column=2)

        # Поля ввода
        ttk.Label(frame, text="Сумма:").grid(row=1, column=0, sticky="w")
        self.amount_entry = ttk.Entry(frame); self.amount_entry.grid(row=1, column=1, columnspan=2)

        ttk.Label(frame, text="Дата (YYYY-MM-DD):").grid(row=2, column=0, sticky="w")
        today = date.today().strftime("%Y-%m-%d")
        self.date_entry = ttk.Entry(frame); self.date_entry.insert(0, today); self.date_entry.grid(row=2, column=1, columnspan=2)

        ttk.Label(frame, text="Категория:").grid(row=3, column=0, sticky="w")
        self.category_entry = ttk.Entry(frame); self.category_entry.grid(row=3, column=1, columnspan=2)

        ttk.Label(frame, text="Комментарий:").grid(row=4, column=0, sticky="w")
        self.comment_entry = ttk.Entry(frame); self.comment_entry.grid(row=4, column=1, columnspan=2)

        # Кнопки
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=5, column=0, columnspan=3, pady=10)
        ttk.Button(buttons_frame, text="Добавить", command=self.add_transaction).pack(side="left", padx=10)
        ttk.Button(buttons_frame, text="Удалить", command=self.remove_selected_transaction).pack(side="left", padx=10)

    def create_filter_section(self):
        """Раздел фильтров"""
        filter_frame = ttk.Labelframe(self, text="Фильтры")
        filter_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        # Поле ввода фильтра по категории
        ttk.Label(filter_frame, text="По категории:").grid(row=0, column=0, sticky="w")
        self.category_filter_var = tk.StringVar()
        self.category_filter_entry = ttk.Entry(filter_frame, textvariable=self.category_filter_var)
        self.category_filter_entry.grid(row=0, column=1)

        # Кнопки
        ttk.Button(filter_frame, text="Применить", command=self.apply_category_filter).grid(row=0, column=2)
        ttk.Button(filter_frame, text="Снять фильтр", command=self.clear_filter).grid(row=0, column=3)

    def create_transactions_list(self):
        """Таблица истории транзакций"""
        list_frame = ttk.Labelframe(self, text="Транзакции")
        list_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        # Дерево транзакций
        self.transactions_tree = ttk.Treeview(list_frame, columns=("Amount", "Type", "Date", "Category", "Comment"))
        self.transactions_tree.heading("#0", text="№")
        for col in ("Amount", "Type", "Date", "Category", "Comment"):
            self.transactions_tree.heading(col, text=col, command=lambda _col=col: self.sort_column(_col))
            self.transactions_tree.column(col, width=150)

        self.transactions_tree.pack(side="left", fill="y")

        # Прокрутка дерева
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.transactions_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.transactions_tree.configure(yscrollcommand=scrollbar.set)

        # Связывание события клика с выбором транзакции
        self.transactions_tree.bind("<ButtonRelease-1>", self.on_select)
        self.selected_index = None

    def sort_column(self, col_name, reverse=False):
        """Сортировка таблицы по столбцам"""
        items = [(self.transactions_tree.set(child_id, col_name), child_id) for child_id in self.transactions_tree.get_children()]
        items.sort(reverse=reverse)
        for i, (_, child_id) in enumerate(items):
            self.transactions_tree.move(child_id, "", i)
        self.sort_directions[col_name] = not reverse

    def create_balance_display(self):
        """Метка текущего баланса"""
        self.balance_label = ttk.Label(self, text="", font=("Arial", 14))
        self.balance_label.pack(pady=10)
        self.update_balance_display()

    def add_transaction(self):
        """Добавление новой транзакции"""
        amount = self.amount_entry.get()
        transaction_type = self.transaction_type_var.get()
        date = self.date_entry.get()
        category = self.category_entry.get()
        comment = self.comment_entry.get()

        # Проверка правильности данных
        errors = validate_transaction(amount, transaction_type, date, category, comment)
        if errors:
            messagebox.showerror("Ошибка", "\n".join(errors))
            return

        # Преобразуем сумму в число
        amount_value = float(amount)

        # Добавляем транзакцию
        self.logic_manager.add_transaction(amount_value, transaction_type, date, category, comment)
        self.update_transactions_list()
        self.update_balance_display()

        # Очищаем поля ввода
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.comment_entry.delete(0, tk.END)

    def remove_selected_transaction(self):
        """Удаление выбранной транзакции"""
        if self.selected_index is not None:
            confirm = messagebox.askyesno("Подтверждение", "Удалить транзакцию?")
            if confirm:
                self.logic_manager.delete_transaction(self.selected_index)
                self.update_transactions_list()
                self.update_balance_display()
                self.selected_index = None
        else:
            messagebox.showwarning("Внимание", "Сначала выберите транзакцию.")

    def on_select(self, event):
        """Обработчик выбора строки в таблице"""
        item = self.transactions_tree.selection()[0]
        self.selected_index = int(self.transactions_tree.item(item)["text"]) - 1

    def apply_category_filter(self):
        """Применение фильтра по категории"""
        category = self.category_filter_var.get()
        if category:
            filtered_data = self.logic_manager.filter_by_category(category)
            self.update_transactions_list(filtered_data)
        else:
            self.update_transactions_list()

    def clear_filter(self):
        """Снятие активного фильтра"""
        self.category_filter_var.set("")
        self.update_transactions_list()

    def update_transactions_list(self, filtered_data=None):
        """Обновление таблицы транзакций"""
        if filtered_data is None:
            transactions = self.logic_manager.get_all_transactions()
        else:
            transactions = filtered_data

        # Очищаем дерево
        self.transactions_tree.delete(*self.transactions_tree.get_children())

        # Добавляем строки заново
        for idx, row in transactions.iterrows():
            self.transactions_tree.insert("", "end", text=str(idx + 1), values=tuple(row))

    def update_balance_display(self):
        """Обновление отображаемого баланса"""
        balance = self.logic_manager.calculate_balance()
        color = "green" if balance >= 0 else "red"
        self.balance_label.config(text=f"Баланс: {balance:.2f}", foreground=color)

    def plot_income_vs_expenses(self):
        """Гистограмма доходов и расходов"""
        self.logic_manager.plot_income_vs_expenses_over_time()

    def plot_pie_chart_categories(self):
        """Круговая диаграмма категорий расходов"""
        self.logic_manager.plot_pie_chart_categories()

    def plot_top_expenses(self):
        """Столбчатый график крупных расходов"""
        self.logic_manager.plot_bar_chart_top_expenses()