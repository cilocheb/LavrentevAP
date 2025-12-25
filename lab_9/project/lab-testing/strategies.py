"""Стратегии расчета зарплаты для разных типов сотрудников."""

from abc import ABC, abstractmethod


class SalaryCalculationStrategy(ABC):
    """Интерфейс для стратегии расчета зарплаты."""

    @abstractmethod
    def calculate(self, employee) -> float:
        """Расчет зарплаты сотрудника.

        Args:
            employee: Объект сотрудника

        Returns:
            float: Размер зарплаты
        """
        pass


class BaseSalaryStrategy(SalaryCalculationStrategy):
    """Базовая зарплата без каких-либо бонусов."""

    def calculate(self, employee) -> float:
        """Возвращает только базовую зарплату.

        Args:
            employee: Объект сотрудника

        Returns:
            float: Базовая зарплата
        """
        return employee.base_salary


class ManagerSalaryStrategy(SalaryCalculationStrategy):
    """Зарплата менеджера с бонусом."""

    def calculate(self, employee) -> float:
        """Базовая зарплата + бонус.

        Args:
            employee: Объект сотрудника (Manager)

        Returns:
            float: Зарплата с бонусом
        """
        return employee.base_salary + getattr(employee, "bonus", 0)


class DeveloperSalaryStrategy(SalaryCalculationStrategy):
    """Зарплата разработчика с учетом уровня."""

    def calculate(self, employee) -> float:
        """Расчет зарплаты разработчика по уровню.

        Args:
            employee: Объект сотрудника (Developer)

        Returns:
            float: Зарплата с коэффициентом по уровню
        """
        level_multipliers = {"junior": 1.0, "middle": 1.5, "senior": 2.0}
        multiplier = level_multipliers.get(getattr(employee, "level", "junior"), 1.0)
        return employee.base_salary * multiplier


class SalespersonSalaryStrategy(SalaryCalculationStrategy):
    """Зарплата продавца с комиссией."""

    def calculate(self, employee) -> float:
        """Базовая зарплата + комиссия от продаж.

        Args:
            employee: Объект сотрудника (Salesperson)

        Returns:
            float: Зарплата с комиссией
        """
        base = employee.base_salary
        commission_rate = getattr(employee, "commission", 0)
        sales = getattr(employee, "sales", 0)
        return base + (sales * commission_rate)
