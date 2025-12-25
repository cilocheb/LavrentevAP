import pytest
from employee import Employee


class TestEmployeeCreation:
    """Тестирование создания Employee"""

    def test_employee_creation_valid_data(self):
        """Тест 1: Создание с валидными данными"""
        emp = Employee(1, "Alice", "IT", 5000)

        assert emp.id == 1
        assert emp.name == "Alice"
        assert emp.department == "IT"
        assert emp.base_salary == 5000


class TestEmployeeValidation:
    """Тестирование валидации"""

    def test_invalid_id_negative(self):
        """Тест 2: Отрицательный ID вызывает ошибку"""
        with pytest.raises(ValueError):
            Employee(-1, "Alice", "IT", 5000)

    def test_empty_name(self):
        """Тест 3: Пустое имя вызывает ошибку"""
        with pytest.raises(ValueError):
            Employee(1, "", "IT", 5000)

    def test_negative_salary(self):
        """Тест 4: Отрицательная зарплата вызывает ошибку"""
        with pytest.raises(ValueError):
            Employee(1, "Alice", "IT", -5000)


class TestEmployeeMethods:
    """Тестирование методов"""

    def test_calculate_salary(self):
        """Тест 5: Расчет зарплаты базового сотрудника"""
        emp = Employee(1, "Alice", "IT", 5000)
        assert emp.calculate_salary() == 5000

    def test_str_representation(self):
        """Тест 6: Строковое представление"""
        emp = Employee(1, "Alice", "IT", 5000)
        result = str(emp)

        assert "Alice" in result
        assert "5000" in result
