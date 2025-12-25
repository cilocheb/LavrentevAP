import pytest
from employee import Employee, Developer
from patterns import SingletonDatabase, EmployeeBuilder, BonusDecorator, EmployeeRepository


class TestSingleton:
    """Тестирование Singleton"""

    def test_singleton_same_instance(self):
        """Тест: Один экземпляр"""
        db1 = SingletonDatabase.get_instance()
        db2 = SingletonDatabase.get_instance()

        assert db1 is db2
        assert id(db1) == id(db2)


class TestBuilder:
    """Тестирование Builder"""

    def test_employee_builder(self):
        """Тест: Построение через Builder"""
        developer = (EmployeeBuilder()
                     .set_id(101)
                     .set_name("John Doe")
                     .set_department("DEV")
                     .set_base_salary(5000)
                     .set_skills(["Python", "Java"])
                     .set_seniority("senior")
                     .build())

        assert developer.id == 101
        assert developer.name == "John Doe"
        assert isinstance(developer, Developer)


class TestDecorator:
    """Тестирование Decorator"""

    def test_bonus_decorator(self):
        """Тест: Decorator добавляет бонус"""
        emp = Employee(1, "John", "IT", 5000)
        decorated = BonusDecorator(emp, 1000)

        assert decorated.calculate_salary() == 6000


class TestRepository:
    """Тестирование Repository"""

    def test_repository_add_and_find(self):
        """Тест: Добавление и поиск"""
        repo = EmployeeRepository()
        emp = Employee(1, "John", "IT", 5000)

        repo.add(emp)
        found = repo.find_by_id(1)

        assert found is not None
        assert found.name == "John"
