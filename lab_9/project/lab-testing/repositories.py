"""Интерфейсы и реализации хранилищ данных."""

from abc import ABC, abstractmethod
from typing import Any, List, Optional


class EmployeeRepository(ABC):
    """Интерфейс для работы с хранилищем сотрудников."""

    @abstractmethod
    def get_employee(self, emp_id: int) -> Optional[Any]:
        """Получить сотрудника по ID."""

    @abstractmethod
    def save_employee(self, employee: Any) -> None:
        """Сохранить сотрудника."""

    @abstractmethod
    def get_all_employees(self) -> List[Any]:
        """Получить всех сотрудников."""

    @abstractmethod
    def delete_employee(self, emp_id: int) -> bool:
        """Удалить сотрудника."""


class InMemoryEmployeeRepository(EmployeeRepository):
    """Реализация хранилища в памяти (для тестов)."""

    def __init__(self):
        """Инициализация пустого словаря."""
        self.employees = {}

    def get_employee(self, emp_id: int) -> Optional[Any]:
        """Получить из памяти."""
        return self.employees.get(emp_id)

    def save_employee(self, employee: Any) -> None:
        """Сохранить в память."""
        self.employees[employee.id] = employee

    def get_all_employees(self) -> List[Any]:
        """Получить все из памяти."""
        return list(self.employees.values())

    def delete_employee(self, emp_id: int) -> bool:
        """Удалить из памяти."""
        if emp_id in self.employees:
            del self.employees[emp_id]
            return True
        return False


class FileEmployeeRepository(EmployeeRepository):
    """Реализация хранилища в файле (CSV)."""

    def __init__(self, filename: str = "employees.csv"):
        """Инициализация с файлом."""
        self.filename = filename
        self.employees = {}

    def get_employee(self, emp_id: int) -> Optional[Any]:
        """Получить из файла."""
        return self.employees.get(emp_id)

    def save_employee(self, employee: Any) -> None:
        """Сохранить в файл."""
        self.employees[employee.id] = employee

    def get_all_employees(self) -> List[Any]:
        """Получить все из файла."""
        return list(self.employees.values())

    def delete_employee(self, emp_id: int) -> bool:
        """Удалить из файла."""
        if emp_id in self.employees:
            del self.employees[emp_id]
            return True
        return False
