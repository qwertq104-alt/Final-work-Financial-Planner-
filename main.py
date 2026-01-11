# main.py
from view_tkinter import FinancialApp  # Интерфейс приложения
from controller import FinancialController  # Логика взаимодействия с данными
from business_logic import TransactionManager  # Управление транзакциями

# Точка входа в приложение
if __name__ == "__main__":
    # Создаем контроллер, подключенный к файлу с транзакциями
    controller = FinancialController("data/transactions.csv")

    # Инициализируем менеджер транзакций, который управляется контроллером
    logic_manager = TransactionManager(controller)

    # Создаем окно интерфейса приложения, связанное с менеджером транзакций
    app = FinancialApp(logic_manager)

    # Запускаем главное событие Tkinter — запускает интерфейс и ждёт ввода пользователя
    app.mainloop()