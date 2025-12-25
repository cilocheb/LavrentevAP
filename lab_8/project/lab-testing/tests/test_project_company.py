import pytest
from company import Company
from project import Project
from department import Department
from employee import Employee, Manager, Developer, Salesperson


class TestCompany:
    """Тестирование Company"""

    def test_add_department(self):
        """Тест: Добавление отдела"""
        company = Company("TechCorp")
        dept = Department("Development")

        company.add_department(dept)

        assert len(company.get_departments()) == 1

    def test_remove_empty_department(self):
        """Тест: Удаление пустого отдела"""
        company = Company("TechCorp")
        dept = Department("Development")

        company.add_department(dept)
        company.remove_department("Development")

        assert len(company.get_departments()) == 0

    def test_cannot_delete_department_with_employees(self):
        """Тест: Нельзя удалить отдел с сотрудниками"""
        company = Company("TechCorp")
        dept = Department("Development")
        emp = Employee(1, "John", "DEV", 5000)

        dept.add_employee(emp)
        company.add_department(dept)

        with pytest.raises(ValueError, match="Cannot delete"):
            company.remove_department("Development")

    def test_find_employee(self):
        """Тест: Поиск сотрудника"""
        company = Company("TechCorp")
        dept = Department("Development")
        emp = Employee(1, "John", "DEV", 5000)

        dept.add_employee(emp)
        company.add_department(dept)

        found = company.find_employee_by_id(1)

        assert found is not None
        assert found.name == "John"

    def test_complex_company_structure(self):
        """Тест: Интеграционный тест"""
        company = Company("TechInnovations")

        dev_dept = Department("Development")
        sales_dept = Department("Sales")

        mgr = Manager(1, "Alice", "DEV", 7000, 2000)
        dev = Developer(2, "Bob", "DEV", 5000, ["Python"], "senior")
        sales = Salesperson(3, "Charlie", "SAL", 4000, 0.15, 50000)

        dev_dept.add_employee(mgr)
        dev_dept.add_employee(dev)
        sales_dept.add_employee(sales)

        company.add_department(dev_dept)
        company.add_department(sales_dept)

        assert len(company.get_all_employees()) == 3
        assert company.calculate_total_monthly_cost() == 30500


class TestProject:
    """Тестирование Project"""

    def test_add_team_member(self):
        """Тест: Добавление в команду"""
        proj = Project(1, "AI Platform", "Разработка AI", "2024-12-31", "planning")
        dev = Developer(1, "John", "DEV", 5000, ["Python"], "senior")

        proj.add_team_member(dev)

        assert proj.get_team_size() == 1

    def test_project_total_salary(self):
        """Тест: Полиморфный расчет"""
        proj = Project(1, "AI", "AI", "2024-12-31", "planning")

        mgr = Manager(1, "Alice", "DEV", 7000, 2000)
        dev = Developer(2, "Bob", "DEV", 5000, ["Python"], "senior")

        proj.add_team_member(mgr)
        proj.add_team_member(dev)

        assert proj.calculate_total_salary() == 19000
