"""Отдел компании с управлением сотрудниками."""

from typing import List, Optional, Iterator
from employee import Employee


class Department:
    """Отдел компании с сотрудниками."""

    def __init__(self, name: str):
        """Инициализация отдела.

        Args:
            name: Название отдела
        """
        self.name = name
        self.employees: List[Employee] = []

    def add_employee(self, employee: Employee) -> None:
        """Добавить сотрудника в отдел.

        Args:
            employee: Объект сотрудника
        """
        if employee not in self.employees:
            self.employees.append(employee)

    def remove_employee(self, employee: Employee) -> None:
        """Удалить сотрудника из отдела.

        Args:
            employee: Объект сотрудника
        """
        if employee in self.employees:
            self.employees.remove(employee)

    def find_employee_by_id(self, emp_id: int) -> Optional[Employee]:
        """Найти сотрудника по ID.

        Args:
            emp_id: ID сотрудника

        Returns:
            Объект сотрудника или None
        """
        for employee in self.employees:
            if employee.id == emp_id:
                return employee
        return None

    def find_employee_by_name(self, name: str) -> Optional[Employee]:
        """Найти сотрудника по имени.

        Args:
            name: Имя сотрудника

        Returns:
            Объект сотрудника или None
        """
        for employee in self.employees:
            if employee.name == name:
                return employee
        return None

    def calculate_total_salary(self) -> float:
        """Расчет общей зарплаты отдела.

        Returns:
            Сумма зарплат всех сотрудников
        """
        return sum(emp.calculate_salary() for emp in self.employees)

    def calculate_average_salary(self) -> float:
        """Расчет средней зарплаты.

        Returns:
            Средняя зарплата или 0
        """
        if not self.employees:
            return 0.0
        return self.calculate_total_salary() / len(self.employees)

    def get_info(self) -> str:
        """Получить информацию об отделе.

        Returns:
            Строка с информацией
        """
        total = self.calculate_total_salary()
        avg = self.calculate_average_salary()
        count = len(self.employees)

        return (
            f"{self.name}: {count} сотр., "
            f"всего зарплата {total} руб., "
            f"средняя {avg:.2f} руб."
        )

    def __len__(self) -> int:
        """Количество сотрудников в отделе."""
        return len(self.employees)

    def __getitem__(self, index: int) -> Employee:
        """Получить сотрудника по индексу.

        Args:
            index: Индекс в списке

        Returns:
            Объект сотрудника

        Raises:
            IndexError: Если индекс вне диапазона
        """
        return self.employees[index]

    def __contains__(self, employee: Employee) -> bool:
        """Проверить наличие сотрудника в отделе.

        Args:
            employee: Объект сотрудника

        Returns:
            True если есть, False иначе
        """
        return employee in self.employees

    def __iter__(self) -> Iterator[Employee]:
        """Итератор по сотрудникам отдела.

        Yields:
            Объекты Employee
        """
        return iter(self.employees)

    def __str__(self) -> str:
        """Строковое представление отдела."""
        return self.get_info()

    def __repr__(self) -> str:
        """Представление для отладки."""
        return f"Department(name='{self.name}', employees={len(self.employees)})"
