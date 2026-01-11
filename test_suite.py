# test_suite.py
import unittest
import tempfile
import pandas as pd
from model import FinancialModel
from business_logic import BusinessLogic
from validation import validate_transaction

# Юнит-тесты
class TestFinancialApp(unittest.TestCase):
    def setUp(self):
        # Создаем временный файл для хранения данных в процессе тестирования
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.csv', mode='w+', encoding='utf-8', delete=False)
        headers = ["Amount", "Type", "Date", "Category", "Comment"]
        pd.DataFrame(columns=headers).to_csv(self.temp_file.name, index=False)
        self.model = FinancialModel(self.temp_file.name)
        self.logic = BusinessLogic(self.model)

        # Очищаем данные перед каждым новым тестом
        self.model.clean_data()

    def tearDown(self):
        # Закрываем и удаляем временный файл после окончания теста
        self.temp_file.close()
        import os
        os.unlink(self.temp_file.name)

    def test_add_transaction(self):
        # Добавляем новую транзакцию
        self.logic.add_transaction(1000, 'Income', '2026-01-01', 'Зарплата', '')

        # Проверяем наличие категории в данных
        data = self.model.get_data()
        self.assertIn('Зарплата', data['Category'].values, "Категория не добавлена!")

    def test_delete_transaction(self):
        # Проверяем удаление транзакции
        self.logic.add_transaction(1000, 'Income', '2026-01-01', 'Зарплата', '')
        last_index = len(self.model.get_data()) - 1
        self.logic.delete_transaction(last_index)
        data = self.model.get_data()
        self.assertNotIn('Зарплата', data['Category'], "Транзакция не удалена!")

    def test_calculate_balance(self):
        # Проверяем расчет баланса
        self.logic.add_transaction(1000, 'Income', '2026-01-01', 'Зарплата', '')
        self.logic.add_transaction(500, 'Expense', '2026-01-01', 'Расходы', '')
        balance = self.logic.calculate_balance()
        self.assertEqual(balance, 500, "Баланс подсчитан некорректно!")

    def test_validation_errors(self):
        # Проверяем обнаружение ошибок валидации
        errors = validate_transaction('-1000', 'Invalid Type', 'bad-date', 'invalid-category', '')
        self.assertGreater(len(errors), 0, "Ошибка валидации не выявилась!")

    def test_valid_transaction(self):
        # Проверяем успешную обработку корректной транзакции
        errors = validate_transaction('1000', 'Income', '2026-01-02', 'Зарплата', '')
        self.assertFalse(errors, "Корректная транзакция вызывает ошибку!")

# Экспорт функции для запуска всех тестов
def run_all_tests():
    """
    Запускает все юнит-тесты и возвращает результаты.
    """
    test_loader = unittest.TestLoader()
    test_suite = test_loader.loadTestsFromTestCase(TestFinancialApp)
    test_runner = unittest.TextTestRunner(verbosity=2)  # Подробный вывод результата
    result = test_runner.run(test_suite)

    # Возвращаем статистику выполнения тестов
    total_tests = result.testsRun
    success_count = total_tests - len(result.failures) - len(result.errors)
    failure_count = len(result.failures)
    error_count = len(result.errors)
    return total_tests, success_count, failure_count, error_count