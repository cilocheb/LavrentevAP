"""Паттерны проектирования (Singleton, Builder, Decorator, Repository)."""

from typing import Dict, Optional
from abc import ABC, abstractmethod
from employee import Employee


class SingletonMeta(type):
    """Метакласс для реализации паттерна Singleton."""

    _instances: Dict = {}

    def __call__(cls, *args, **kwargs):
        """Переопределение создания экземпляра.

        Returns:
            Единственный экземпляр класса
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonDatabase(metaclass=SingletonMeta):
    """Синглтон база данных - Singleton паттерн."""

    def __init__(self) -> None:
        """Инициализация синглтона."""
        self.data: Dict = {}

    @classmethod
    def get_instance(cls) -> "SingletonDatabase":
        """Получить единственный экземпляр.

        Returns:
            Единственный экземпляр SingletonDatabase
        """
        return cls()

    def add(self, key: str, value) -> None:
        """Добавить данные.

        Args:
            key: Ключ
            value: Значение
        """
        self.data[key] = value

    def get(self, key: str):
        """Получить данные по ключу.

        Args:
            key: Ключ

        Returns:
            Значение или None
        """
        return self.data.get(key)


class EmployeeBuilder:
    """Builder паттерн для создания сотрудников."""

    def __init__(self) -> None:
        """Инициализация строителя."""
        self.emp_id: Optional[int] = None
        self.name: Optional[str] = None
        self.department: Optional[str] = None
        self.base_salary: Optional[float] = None
        self.bonus: Optional[float] = None
        self.skills: Optional[list] = None
        self.level: Optional[str] = None
        self.seniority: Optional[str] = None
        self.commission: Optional[float] = None
        self.sales: Optional[float] = None

    def set_id(self, emp_id: int) -> "EmployeeBuilder":
        """Установить ID.

        Args:
            emp_id: ID сотрудника

        Returns:
            Self для chain-вызовов
        """
        self.emp_id = emp_id
        return self

    def set_name(self, name: str) -> "EmployeeBuilder":
        """Установить имя.

        Args:
            name: Имя сотрудника

        Returns:
            Self для chain-вызовов
        """
        self.name = name
        return self

    def set_department(self, department: str) -> "EmployeeBuilder":
        """Установить отдел.

        Args:
            department: Название отдела

        Returns:
            Self для chain-вызовов
        """
        self.department = department
        return self

    def set_base_salary(self, salary: float) -> "EmployeeBuilder":
        """Установить базовую зарплату.

        Args:
            salary: Размер зарплаты

        Returns:
            Self для chain-вызовов
        """
        self.base_salary = salary
        return self

    def set_bonus(self, bonus: float) -> "EmployeeBuilder":
        """Установить бонус для менеджера.

        Args:
            bonus: Размер бонуса

        Returns:
            Self для chain-вызовов
        """
        self.bonus = bonus
        return self

    def set_skills(self, skills: list) -> "EmployeeBuilder":
        """Установить навыки.

        Args:
            skills: Список навыков

        Returns:
            Self для chain-вызовов
        """
        self.skills = skills
        return self

    def set_level(self, level: str) -> "EmployeeBuilder":
        """Установить уровень.

        Args:
            level: Уровень квалификации

        Returns:
            Self для chain-вызовов
        """
        self.level = level
        return self

    def set_seniority(self, seniority: str) -> "EmployeeBuilder":
        """Установить seniorityность.

        Args:
            seniority: Уровень senior (alias for level)

        Returns:
            Self для chain-вызовов
        """
        self.seniority = seniority
        self.level = seniority
        return self

    def set_commission(self, commission: float) -> "EmployeeBuilder":
        """Установить комиссию.

        Args:
            commission: Размер комиссии

        Returns:
            Self для chain-вызовов
        """
        self.commission = commission
        return self

    def set_sales(self, sales: float) -> "EmployeeBuilder":
        """Установить продажи.

        Args:
            sales: Сумма продаж

        Returns:
            Self для chain-вызовов
        """
        self.sales = sales
        return self

    def build(self) -> Employee:
        """Построить объект сотрудника.

        Returns:
            Объект Employee

        Raises:
            ValueError: Если обязательные параметры не установлены
        """
        if (
            self.emp_id is None
            or self.name is None
            or self.department is None
            or self.base_salary is None
        ):
            raise ValueError(
                "Не установлены обязательные параметры "
                "(ID, name, department, base_salary)"
            )

        from employee import Manager, Developer, Salesperson

        if self.bonus is not None:
            return Manager(
                self.emp_id,
                self.name,
                self.department,
                self.base_salary,
                self.bonus,
            )

        if self.level is not None or self.seniority is not None:
            return Developer(
                self.emp_id,
                self.name,
                self.department,
                self.base_salary,
                self.skills or [],
                self.level or self.seniority or "junior",
            )

        if self.commission is not None:
            return Salesperson(
                self.emp_id,
                self.name,
                self.department,
                self.base_salary,
                self.commission,
                self.sales or 0,
            )

        return Employee(self.emp_id, self.name, self.department, self.base_salary)


class EmployeeDecorator:
    """Decorator паттерн для добавления функциональности к сотруднику."""

    def __init__(self, employee: Employee) -> None:
        """Инициализация декоратора.

        Args:
            employee: Сотрудник для декорирования
        """
        self.employee = employee

    def calculate_salary(self) -> float:
        """Получить зарплату декорированного сотрудника.

        Returns:
            Размер зарплаты
        """
        return self.employee.calculate_salary()

    def get_info(self) -> str:
        """Получить информацию о сотруднике.

        Returns:
            Строка с информацией
        """
        return self.employee.get_info()


class BonusDecorator(EmployeeDecorator):
    """Добавляет премию к зарплате."""

    def __init__(self, employee: Employee, bonus_amount: float) -> None:
        """Инициализация.

        Args:
            employee: Сотрудник
            bonus_amount: Размер дополнительной премии
        """
        super().__init__(employee)
        self.bonus_amount = bonus_amount

    def calculate_salary(self) -> float:
        """Зарплата + дополнительная премия.

        Returns:
            Размер зарплаты с премией
        """
        return self.employee.calculate_salary() + self.bonus_amount

    def get_info(self) -> str:
        """Информация с примечанием о премии.

        Returns:
            Строка с информацией
        """
        return f"{self.employee.get_info()} + премия {self.bonus_amount}"


class EmployeeRepository(ABC):
    """Интерфейс для хранилища сотрудников."""

    @abstractmethod
    def add(self, employee: Employee) -> None:
        """Добавить сотрудника.

        Args:
            employee: Объект сотрудника
        """
        pass

    @abstractmethod
    def find_by_id(self, emp_id: int) -> Optional[Employee]:
        """Найти сотрудника по ID.

        Args:
            emp_id: ID сотрудника

        Returns:
            Объект сотрудника или None
        """
        pass

    @abstractmethod
    def get_all(self) -> list:
        """Получить всех сотрудников.

        Returns:
            Список сотрудников
        """
        pass


class InMemoryEmployeeRepository(EmployeeRepository):
    """Хранилище сотрудников в памяти."""

    def __init__(self) -> None:
        """Инициализация хранилища."""
        self.employees: Dict[int, Employee] = {}

    def add(self, employee: Employee) -> None:
        """Добавить сотрудника.

        Args:
            employee: Объект сотрудника
        """
        self.employees[employee.id] = employee

    def find_by_id(self, emp_id: int) -> Optional[Employee]:
        """Найти сотрудника по ID.

        Args:
            emp_id: ID сотрудника

        Returns:
            Объект сотрудника или None
        """
        return self.employees.get(emp_id)

    def get_all(self) -> list:
        """Получить всех сотрудников.

        Returns:
            Список сотрудников
        """
        return list(self.employees.values())
