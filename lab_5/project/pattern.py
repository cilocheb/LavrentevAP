from abc import ABC, abstractmethod
from typing import List
import sqlite3

# ==================== БАЗОВЫЕ КЛАССЫ ====================

class Employee:
    """Базовый класс сотрудника с инкапсуляцией"""
    
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float):
        self.__id = None
        self.__name = None
        self.__department = None
        self.__base_salary = None
        self.id = emp_id
        self.name = name
        self.department = department
        self.base_salary = base_salary

    @property
    def id(self) -> int:
        return self.__id
    @id.setter
    def id(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID должен быть положительным")
        self.__id = value

    @property
    def name(self) -> str:
        return self.__name
    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Имя должно быть непустым")
        self.__name = value.strip()

    @property
    def department(self) -> str:
        return self.__department
    @department.setter
    def department(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Отдел должен быть непустым")
        self.__department = value.strip()

    @property
    def base_salary(self) -> float:
        return self.__base_salary
    @base_salary.setter
    def base_salary(self, value: float) -> None:
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Зарплата должна быть положительной")
        self.__base_salary = float(value)

    def __str__(self) -> str:
        return f"S[id:{self.id}, {self.name}, {self.department}, {self.base_salary}]"

class AbstractEmployee(Employee, ABC):
    """Абстрактный класс для всех сотрудников"""
    
    @abstractmethod
    def calculate_salary(self) -> float:
        pass

    @abstractmethod
    def get_info(self) -> str:
        pass

class Manager(AbstractEmployee):
    """Менеджер - зарплата = базовая + бонус"""
    
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float, bonus: float):
        super().__init__(emp_id, name, department, base_salary)
        self.__bonus = bonus
    
    def calculate_salary(self) -> float:
        return self.base_salary + self.__bonus
    
    def get_info(self) -> str:
        return f"Manager {self.name}: {self.calculate_salary()}"

class Developer(AbstractEmployee):
    """Разработчик - зарплата = базовая * коэффициент сеньорности"""
    
    SENIORITY = {"junior": 1.0, "middle": 1.5, "senior": 2.0}
    
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float, level: str):
        super().__init__(emp_id, name, department, base_salary)
        self.__level = level
    
    def calculate_salary(self) -> float:
        return self.base_salary * self.SENIORITY[self.__level]
    
    def get_info(self) -> str:
        return f"Developer {self.name} ({self.__level}): {self.calculate_salary()}"

class Department:
    """Отдел с управлением сотрудниками"""
    
    def __init__(self, name: str):
        self.name = name
        self.__employees: List[AbstractEmployee] = []
    
    def add_employee(self, employee: AbstractEmployee) -> None:
        self.__employees.append(employee)
    
    def get_employees(self) -> List[AbstractEmployee]:
        return self.__employees[:]

# ==================== ПАТТЕРН 1: SINGLETON ====================

class DatabaseConnection:
    """Singleton - гарантирует одно подключение"""
    
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__connection = None
        return cls.__instance
    
    def get_connection(self):
        if self.__connection is None:
            self.__connection = sqlite3.connect(':memory:')
        return self.__connection

# ==================== ПАТТЕРН 2: FACTORY METHOD ====================

class EmployeeFactory:
    """Factory Method - создание сотрудников"""
    
    @staticmethod
    def create_employee(emp_type: str, **kwargs) -> AbstractEmployee:
        if emp_type == "manager":
            return Manager(**kwargs)
        elif emp_type == "developer":
            return Developer(**kwargs)
        else:
            raise ValueError("Неизвестный тип")

# ==================== ПАТТЕРН 3: BUILDER ====================

class EmployeeBuilder:
    """Builder - пошаговое построение (Fluent Interface)"""
    
    def __init__(self):
        self.__data = {}
    
    def set_id(self, emp_id: int) -> 'EmployeeBuilder':
        self.__data['emp_id'] = emp_id
        return self
    
    def set_name(self, name: str) -> 'EmployeeBuilder':
        self.__data['name'] = name
        return self
    
    def set_department(self, department: str) -> 'EmployeeBuilder':
        self.__data['department'] = department
        return self
    
    def set_base_salary(self, salary: float) -> 'EmployeeBuilder':
        self.__data['base_salary'] = salary
        return self
    
    def set_type(self, emp_type: str) -> 'EmployeeBuilder':
        self.__data['type'] = emp_type
        return self
    
    def set_level(self, level: str) -> 'EmployeeBuilder':
        self.__data['level'] = level
        return self
    
    def set_bonus(self, bonus: float) -> 'EmployeeBuilder':
        self.__data['bonus'] = bonus
        return self
    
    def build(self) -> AbstractEmployee:
        emp_type = self.__data.get('type')
        
        if emp_type == "developer":
            return Developer(
                self.__data['emp_id'],
                self.__data['name'],
                self.__data['department'],
                self.__data['base_salary'],
                self.__data.get('level', 'junior')
            )
        elif emp_type == "manager":
            return Manager(
                self.__data['emp_id'],
                self.__data['name'],
                self.__data['department'],
                self.__data['base_salary'],
                self.__data.get('bonus', 0)
            )
        raise ValueError("Неполные данные")

# ==================== ПАТТЕРН 4: DECORATOR ====================

class SalaryDecorator(ABC):
    """Абстрактный декоратор для зарплаты"""
    
    def __init__(self, employee: AbstractEmployee):
        self._employee = employee
    
    @abstractmethod
    def calculate_salary(self) -> float:
        pass

class BonusDecorator(SalaryDecorator):
    """Decorator - добавляет фиксированный бонус"""
    
    def __init__(self, employee: AbstractEmployee, bonus_amount: float):
        super().__init__(employee)
        self.__bonus_amount = bonus_amount
    
    def calculate_salary(self) -> float:
        return self._employee.calculate_salary() + self.__bonus_amount

class TrainingDecorator(SalaryDecorator):
    """Decorator - добавляет процент за обучение"""
    
    def __init__(self, employee: AbstractEmployee, training_bonus: float):
        super().__init__(employee)
        self.__training_bonus = training_bonus
    
    def calculate_salary(self) -> float:
        return self._employee.calculate_salary() * (1 + self.__training_bonus)

# ==================== ПАТТЕРН 5: STRATEGY ====================

class BonusStrategy(ABC):
    """Абстрактная стратегия бонуса"""
    
    @abstractmethod
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        pass

class PerformanceBonusStrategy(BonusStrategy):
    """Strategy - бонус за производительность (10%)"""
    
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        return employee.calculate_salary() * 0.1

class ProjectBonusStrategy(BonusStrategy):
    """Strategy - бонус за проекты (5% за каждый)"""
    
    def __init__(self, project_count: int):
        self.__project_count = project_count
    
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        return employee.calculate_salary() * (0.05 * self.__project_count)

# ==================== ПАТТЕРН 6: FACADE ====================

class CompanyFacade:
    """Facade - упрощенный интерфейс для управления компанией"""
    
    def __init__(self):
        self.__departments: List[Department] = []
    
    def create_department(self, name: str) -> Department:
        dept = Department(name)
        self.__departments.append(dept)
        return dept
    
    def hire_employee(self, dept: Department, emp_type: str, emp_id: int,
                     name: str, salary: float, **kwargs) -> AbstractEmployee:
        emp = EmployeeFactory.create_employee(
            emp_type,
            emp_id=emp_id,
            name=name,
            department=dept.name,
            base_salary=salary,
            **kwargs
        )
        dept.add_employee(emp)
        print(f"Нанят: {emp.get_info()}")
        return emp
    
    def get_all_employees(self) -> List[AbstractEmployee]:
        all_emps = []
        for dept in self.__departments:
            all_emps.extend(dept.get_employees())
        return all_emps
    
    def get_total_salary(self) -> float:
        return sum(emp.calculate_salary() for emp in self.get_all_employees())

# ==================== ДЕМОНСТРАЦИЯ ====================


    
    # 1. SINGLETON
    print("\n1. SINGLETON - DatabaseConnection")
    print("-" * 80)
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"db1 is db2: {db1 is db2}")
    print(" Singleton работает: одно подключение\n")
    
    # 2. FACTORY METHOD
    print("2. FACTORY METHOD - EmployeeFactory")
    print("-" * 80)
    dev = EmployeeFactory.create_employee(
        "developer", emp_id=1, name="Иван",
        department="IT", base_salary=60000, level="senior"
    )
    print(f"Создан: {dev.get_info()}")
    print(f"Зарплата: {dev.calculate_salary()}")
    print(" Factory Method работает: создана Developer\n")
    
    # 3. BUILDER
    print("3. BUILDER - Fluent Interface")
    print("-" * 80)
    mgr = (EmployeeBuilder()
        .set_id(2)
        .set_name("Петр")
        .set_department("IT")
        .set_base_salary(70000)
        .set_type("manager")
        .set_bonus(20000)
        .build())
    print(f"Построен: {mgr.get_info()}")
    print(f"Зарплата: {mgr.calculate_salary()}")
    print(" Builder работает: объект построен цепочкой методов\n")
    
    # 4. DECORATOR
    print("4. DECORATOR - Украшение зарплаты")
    print("-" * 80)
    dev_base = dev.calculate_salary()
    decorated = BonusDecorator(dev, 5000)
    decorated = TrainingDecorator(decorated, 0.1)
    print(f"Базовая зарплата: {dev_base}")
    print(f"С бонусом (+5000): {BonusDecorator(dev, 5000).calculate_salary()}")
    print(f"С бонусом и обучением (+10%): {decorated.calculate_salary():.2f}")
    print(" Decorator работает: добавлена функциональность\n")
    
    # 5. STRATEGY
    print("5. STRATEGY - Выбор стратегии бонуса")
    print("-" * 80)
    strategies = [
        ("Производительность (10%)", PerformanceBonusStrategy()),
        ("За проекты (3 проекта = 15%)", ProjectBonusStrategy(3))
    ]
    for name, strategy in strategies:
        bonus = strategy.calculate_bonus(dev)
        total = dev.calculate_salary() + bonus
        print(f"{name}: бонус {bonus:.2f}, итого {total:.2f}")
    print(" Strategy работает: разные стратегии\n")
    
    # 6. FACADE
    print("6. FACADE - Упрощенный интерфейс")
    print("-" * 80)
    facade = CompanyFacade()
    it_dept = facade.create_department("IT")
    
    print("Наем сотрудников через Facade:")
    facade.hire_employee(it_dept, "developer", 10, "Мария", 55000, level="middle")
    facade.hire_employee(it_dept, "manager", 11, "Анна", 75000, bonus=15000)
    
    all_emps = facade.get_all_employees()
    total = facade.get_total_salary()
    print(f"\nВсего сотрудников: {len(all_emps)}")
    print(f"Общая зарплата: {total:.2f}")
    print(" Facade работает: упрощенный интерфейс\n")
    
    # ИТОГИ
    print("=" * 80)
    print(" ВСЕ 6 ПАТТЕРНОВ УСПЕШНО ПРОДЕМОНСТРИРОВАНЫ")
    print("=" * 80)
    print("\nРезультаты:")
    print(" SINGLETON: одно подключение")
    print(" FACTORY: создание сотрудников")
    print(" BUILDER: построение через цепочку методов")
    print(" DECORATOR: добавление функциональности")
    print(" STRATEGY: выбор алгоритма")
    print(" FACADE: упрощенный интерфейс")
    print("\nВся система интегрирована и работает! ")
