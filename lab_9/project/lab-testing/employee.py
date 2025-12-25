"""Модели сотрудников компании."""

from validators import EmployeeValidator
from strategies import (
    SalaryCalculationStrategy,
    BaseSalaryStrategy,
    ManagerSalaryStrategy,
    DeveloperSalaryStrategy,
    SalespersonSalaryStrategy,
)


class Employee:
    """Базовый класс сотрудника."""

    def __init__(
        self,
        emp_id: int,
        name: str,
        department: str,
        base_salary: float,
        salary_strategy: SalaryCalculationStrategy = None,
    ):
        """Инициализация сотрудника.

        Args:
            emp_id: Уникальный ID
            name: Полное имя
            department: Отдел
            base_salary: Базовая зарплата
            salary_strategy: Стратегия расчета зарплаты
        """
        EmployeeValidator.validate_employee(emp_id, name, base_salary)

        self.id = emp_id
        self.name = name
        self.department = department
        self.base_salary = base_salary
        self.salary_strategy = salary_strategy or BaseSalaryStrategy()

    def calculate_salary(self) -> float:
        """Расчет зарплаты через стратегию."""
        return self.salary_strategy.calculate(self)

    def get_info(self) -> str:
        """Получить информацию о сотруднике."""
        return f"{self.name} ({self.department}): " f"{self.calculate_salary()} руб."

    def __str__(self) -> str:
        """Строковое представление."""
        return self.get_info()

    def __eq__(self, other: "Employee") -> bool:
        """Сравнение по ID."""
        if not isinstance(other, Employee):
            return False
        return self.id == other.id

    def __lt__(self, other: "Employee") -> bool:
        """Сравнение по зарплате."""
        if not isinstance(other, Employee):
            return NotImplemented
        return self.calculate_salary() < other.calculate_salary()

    def __add__(self, other: "Employee") -> float:
        """Сложение зарплат."""
        if not isinstance(other, Employee):
            return NotImplemented
        return self.calculate_salary() + other.calculate_salary()


class Manager(Employee):
    """Менеджер с бонусом."""

    def __init__(
        self,
        emp_id: int,
        name: str,
        department: str,
        base_salary: float,
        bonus: float,
    ):
        """Инициализация менеджера.

        Args:
            emp_id: Уникальный ID
            name: Имя
            department: Отдел
            base_salary: Базовая зарплата
            bonus: Бонус
        """
        super().__init__(emp_id, name, department, base_salary, ManagerSalaryStrategy())
        self.bonus = bonus

    def get_info(self) -> str:
        """Получить информацию о менеджере."""
        return (
            f"{self.name} ({self.department}): "
            f"{self.calculate_salary()} руб. (бонус: {self.bonus})"
        )


class Developer(Employee):
    """Разработчик с уровнем квалификации."""

    def __init__(
        self,
        emp_id: int,
        name: str,
        department: str,
        base_salary: float,
        skills: list,
        level: str,
    ):
        """Инициализация разработчика.

        Args:
            emp_id: Уникальный ID
            name: Имя
            department: Отдел
            base_salary: Базовая зарплата
            skills: Список навыков
            level: Уровень квалификации (junior/middle/senior)
        """
        super().__init__(
            emp_id, name, department, base_salary, DeveloperSalaryStrategy()
        )
        self.skills = skills
        self.level = level

    def add_skill(self, skill: str) -> None:
        """Добавить навык разработчику.

        Args:
            skill: Название навыка
        """
        if skill not in self.skills:
            self.skills.append(skill)

    def get_info(self) -> str:
        """Получить информацию о разработчике."""
        skills_str = ", ".join(self.skills)
        return (
            f"{self.name} ({self.department}, {self.level}): "
            f"{self.calculate_salary()} руб. Навыки: {skills_str}"
        )


class Salesperson(Employee):
    """Продавец с комиссией."""

    def __init__(
        self,
        emp_id: int,
        name: str,
        department: str,
        base_salary: float,
        commission: float,
        sales: float,
    ):
        """Инициализация продавца.

        Args:
            emp_id: Уникальный ID
            name: Имя
            department: Отдел
            base_salary: Базовая зарплата
            commission: Процент комиссии (например 0.15 для 15%)
            sales: Сумма продаж
        """
        super().__init__(
            emp_id,
            name,
            department,
            base_salary,
            SalespersonSalaryStrategy(),
        )
        self.commission = commission
        self.sales = sales

    def get_info(self) -> str:
        """Получить информацию о продавце."""
        return (
            f"{self.name} ({self.department}): "
            f"{self.calculate_salary()} руб. "
            f"(Продажи: {self.sales} руб.)"
        )
