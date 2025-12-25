import pytest
from department import Department
from employee import Employee, Manager, Developer


class TestDepartment:
    """Тестирование Department"""

    def test_add_employee(self):
        """Тест: Добавление сотрудника"""
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)

        dept.add_employee(emp)

        assert len(dept) == 1

    def test_department_len(self):
        """Тест: __len__"""
        dept = Department("IT")
        dept.add_employee(Employee(1, "John", "IT", 5000))
        dept.add_employee(Employee(2, "Jane", "IT", 6000))

        assert len(dept) == 2

    def test_department_getitem(self):
        """Тест: __getitem__"""
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)

        dept.add_employee(emp)

        assert dept[0].name == "John"

    def test_department_contains(self):
        """Тест: __contains__"""
        dept = Department("IT")
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Jane", "IT", 6000)

        dept.add_employee(emp1)

        assert emp1 in dept
        assert emp2 not in dept

    def test_department_iteration(self):
        """Тест: Итерация"""
        dept = Department("IT")
        for i in range(3):
            dept.add_employee(Employee(i + 1, f"Emp{i + 1}", "IT", 5000))

        count = 0
        for emp in dept:
            count += 1

        assert count == 3

    def test_calculate_total_salary_polymorphic(self):
        """Тест: Полиморфный расчет"""
        dept = Department("DEV")
        dept.add_employee(Manager(1, "Alice", "DEV", 7000, 2000))
        dept.add_employee(Developer(2, "Bob", "DEV", 5000, ["Python"], "senior"))

        total = dept.calculate_total_salary()

        assert total == 19000


class TestEmployeeComparison:
    """Тестирование операторов сравнения"""

    def test_employee_equality(self):
        """Тест: == по ID"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(1, "Jane", "HR", 6000)

        assert emp1 == emp2

    def test_employee_less_than(self):
        """Тест: < по зарплате"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Jane", "HR", 6000)

        assert emp1 < emp2

    def test_employee_addition(self):
        """Тест: + сложение зарплат"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Jane", "HR", 6000)

        total = emp1 + emp2

        assert total == 11000
