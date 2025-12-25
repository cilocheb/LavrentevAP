import pytest
from employee import Manager, Developer, Salesperson


class TestManager:
    """Тестирование Manager"""

    def test_manager_salary(self):
        """Тест: Зарплата менеджера = база + бонус"""
        mgr = Manager(1, "John", "Management", 5000, 1000)
        assert mgr.calculate_salary() == 6000

    def test_manager_get_info(self):
        """Тест: Информация содержит бонус"""
        mgr = Manager(1, "John", "Management", 5000, 1000)
        info = mgr.get_info()

        assert "бонус" in info.lower()
        assert "1000" in info


class TestDeveloper:
    """Тестирование Developer"""

    @pytest.mark.parametrize("level,expected", [
        ("junior", 5000),
        ("middle", 7500),
        ("senior", 10000)
    ])
    def test_developer_salary_by_level(self, level, expected):
        """Тест: Зарплата зависит от уровня"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], level)
        assert dev.calculate_salary() == expected

    def test_developer_add_skill(self):
        """Тест: Добавление навыка"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], "junior")

        dev.add_skill("Java")

        assert "Java" in dev.skills
        assert len(dev.skills) == 2


class TestSalesperson:
    """Тестирование Salesperson"""

    def test_salesperson_salary(self):
        """Тест: Зарплата = база + (продажи * комиссия)"""
        sales = Salesperson(1, "Bob", "Sales", 4000, 0.15, 50000)
        assert sales.calculate_salary() == 11500


class TestPolymorphism:
    """Тестирование полиморфизма"""

    def test_polymorphic_calculation(self):
        """Тест: Один метод, разные реализации"""
        employees = [
            Manager(1, "John", "MAN", 5000, 1000),
            Developer(2, "Alice", "DEV", 5000, ["Python"], "senior"),
            Salesperson(3, "Bob", "SAL", 4000, 0.15, 50000)
        ]

        salaries = [emp.calculate_salary() for emp in employees]

        assert salaries == [6000, 10000, 11500]
