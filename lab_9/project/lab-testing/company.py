"""Модель компании и управление сотрудниками."""

from typing import List, Optional
from employee import Employee
from patterns import EmployeeRepository, InMemoryEmployeeRepository


class Department:
    """Отдел компании."""

    def __init__(self, name: str) -> None:
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
        self.employees.append(employee)

    def remove_employee(self, emp_id: int) -> bool:
        """Удалить сотрудника из отдела.

        Args:
            emp_id: ID сотрудника

        Returns:
            True если удалился, False если не найден
        """
        for i, emp in enumerate(self.employees):
            if emp.id == emp_id:
                self.employees.pop(i)
                return True
        return False

    def get_total_salary(self) -> float:
        """Получить общую зарплату всех сотрудников.

        Returns:
            Сумма всех зарплат
        """
        return sum(emp.calculate_salary() for emp in self.employees)

    def get_average_salary(self) -> float:
        """Получить среднюю зарплату.

        Returns:
            Средняя зарплата или 0
        """
        if not self.employees:
            return 0
        return self.get_total_salary() / len(self.employees)

    def __len__(self) -> int:
        """Получить количество сотрудников.

        Returns:
            Количество сотрудников
        """
        return len(self.employees)

    def __getitem__(self, index: int) -> Employee:
        """Получить сотрудника по индексу.

        Args:
            index: Индекс

        Returns:
            Объект сотрудника
        """
        return self.employees[index]

    def __contains__(self, emp_id: int) -> bool:
        """Проверить наличие сотрудника.

        Args:
            emp_id: ID сотрудника

        Returns:
            True если сотрудник есть
        """
        return any(emp.id == emp_id for emp in self.employees)

    def __iter__(self):
        """Итератор по сотрудникам.

        Returns:
            Итератор
        """
        return iter(self.employees)

    def get_info(self) -> str:
        """Получить информацию об отделе.

        Returns:
            Строка с информацией
        """
        return (
            f"Department(name={self.name}, "
            f"employees={len(self.employees)}, "
            f"total_salary={self.get_total_salary()}, "
            f"avg_salary={self.get_average_salary()})"
        )


class Company:
    """Компания с отделами и сотрудниками."""

    def __init__(
        self, name: str, repository: Optional[EmployeeRepository] = None
    ) -> None:
        """Инициализация компании.

        Args:
            name: Название компании
            repository: Хранилище сотрудников (опционально)
        """
        self.name = name
        self.repository = repository or InMemoryEmployeeRepository()
        self.departments: List[Department] = []

    def add_department(self, department: Department) -> None:
        """Добавить отдел в компанию.

        Args:
            department: Объект отдела
        """
        self.departments.append(department)

    def remove_department(self, department) -> None:
        """Удалить отдел (только если пуст).

        Args:
            department: Объект отдела или имя отдела

        Raises:
            ValueError: Если отдел содержит сотрудников
        """
        # Если передана строка, найти отдел по имени
        if isinstance(department, str):
            dept_name = department
            dept = None
            for d in self.departments:
                if d.name == dept_name:
                    dept = d
                    break
            if dept is None:
                raise ValueError(f"Department '{dept_name}' not found")
            department = dept

        if len(department) > 0:
            raise ValueError(
                f"Cannot delete department '{department.name}' " "with employees"
            )
        self.departments.remove(department)

    def get_departments(self) -> List[Department]:
        """Получить все отделы.

        Returns:
            Список отделов
        """
        return self.departments

    def add_employee(self, employee: Employee) -> None:
        """Добавить сотрудника в компанию.

        Args:
            employee: Объект сотрудника
        """
        self.repository.add(employee)

    def find_employee(self, emp_id: int) -> Optional[Employee]:
        """Найти сотрудника по ID.

        Args:
            emp_id: ID сотрудника

        Returns:
            Объект сотрудника или None
        """
        return self.repository.find_by_id(emp_id)

    def find_employee_by_id(self, emp_id: int) -> Optional[Employee]:
        """Найти сотрудника по ID (alias для find_employee).

        Args:
            emp_id: ID сотрудника

        Returns:
            Объект сотрудника или None
        """
        # Сначала ищем в repository
        emp = self.repository.find_by_id(emp_id)
        if emp:
            return emp

        # Если не найден, ищем в отделах
        for dept in self.departments:
            for employee in dept.employees:
                if employee.id == emp_id:
                    return employee
        return None

    def get_all_employees(self) -> List[Employee]:
        """Получить всех сотрудников.

        Returns:
            Список сотрудников
        """
        employees = []
        # Собираем из repository
        employees.extend(self.repository.get_all())
        # Собираем из отделов
        for dept in self.departments:
            for emp in dept.employees:
                if emp not in employees:
                    employees.append(emp)
        return employees

    def get_total_salary(self) -> float:
        """Получить общую зарплату всех сотрудников.

        Returns:
            Сумма всех зарплат
        """
        return sum(emp.calculate_salary() for emp in self.get_all_employees())

    def calculate_total_monthly_cost(self) -> float:
        """Получить общую месячную стоимость.

        Returns:
            Сумма всех зарплат
        """
        return self.get_total_salary()

    def get_info(self) -> str:
        """Получить информацию о компании.

        Returns:
            Строка с информацией
        """
        return (
            f"Company(name={self.name}, "
            f"employees={len(self.get_all_employees())}, "
            f"departments={len(self.departments)}, "
            f"total_salary={self.get_total_salary()})"
        )

    def __str__(self) -> str:
        """Строковое представление.

        Returns:
            Информация о компании
        """
        return self.get_info()

    def __repr__(self) -> str:
        """Представление для отладки.

        Returns:
            Информация о компании
        """
        return self.get_info()


class Project:
    """Проект в компании."""

    def __init__(self, name: str) -> None:
        """Инициализация проекта.

        Args:
            name: Название проекта
        """
        self.name = name
        self.team: List[Employee] = []

    def add_team_member(self, employee: Employee) -> None:
        """Добавить члена команды.

        Args:
            employee: Объект сотрудника
        """
        self.team.append(employee)

    def get_total_salary(self) -> float:
        """Получить общую зарплату команды.

        Returns:
            Сумма зарплат всех членов
        """
        return sum(emp.calculate_salary() for emp in self.team)

    def get_info(self) -> str:
        """Получить информацию о проекте.

        Returns:
            Строка с информацией
        """
        return (
            f"Project(name={self.name}, "
            f"team_size={len(self.team)}, "
            f"total_salary={self.get_total_salary()})"
        )
