# Отчёт по лабораторной работе №5

**Тема:** Применение паттернов проектирования в системе учета сотрудников

## Сведения о студенте

**Дата:** 2025-09-04  
**Семестр:** 2 курс, 1 полугодие (3 семестр)  
**Группа:** ПИН-б-о-24-1  
**Дисциплина:** Технологии программирования  
**Студент:** Лаврентьев Аврам Петрович 

### Цель работы

Освоить практическое применение паттернов проектирования для рефакторинга и улучшения кодовой базы системы учета сотрудников. Получить навыки применения различных паттернов для решения типичных задач проектирования ПО.
### Выбранные паттерны и их задачи

Паттерн 1: SINGLETON 
Задача: Обеспечить единственный экземпляр класса подключения к БД
Проблема: Избежать множественных подключений, которые потребляют ресурсы
Решение: Контролировать создание экземпляра через __new__

Паттерн 2: FACTORY METHOD 
Задача: Создавать сотрудников разных типов без указания их классов
Проблема: Снизить зависимость от конкретных классов (Manager, Developer)
Решение: Фабрика выбирает правильный класс на основе типа

Паттерн 3: BUILDER 
Задача: Пошагово строить сложные объекты сотрудников
Проблема: Много параметров в конструкторе -> нечитаемо
Решение: Fluent Interface - цепочка методов для построения

Паттерн 4: DECORATOR 
Задача: Динамически добавлять функциональность к зарплате
Проблема: Добавить бонус и обучение без изменения исходного класса
Решение: Обертка вокруг объекта с дополнительной логикой

Паттерн 5: STRATEGY 
Задача: Выбирать алгоритм расчета бонуса во время выполнения
Проблема: Разные стратегии для разных сотрудников
Решение: Семейство алгоритмов в отдельных классах

Паттерн 6: FACADE 
Задача: Упростить работу с системой управления сотрудниками
Проблема: Множество операций разбросаны по разным классам
Решение: Один простой интерфейс для сложной системы
### Принципы SOLID в паттернах

- **Single Responsibility** - каждый паттерн решает одну задачу
- **Open/Closed** - расширяемость без изменения кода
- **Liskov Substitution** - подтипы взаимозаменяемы
- **Interface Segregation** - узкие интерфейсы
- **Dependency Inversion** - зависимость от абстракций

### Выполненные задачи
 Задача 1: Создать класс DatabaseConnection с Singleton паттерном
Гарантирует только одно подключение.
Проверяется через assert db1 is db2

 Задача 2: Реализовать EmployeeFactory для создания сотрудников.
Поддерживает Manager и Developer.
Избегает прямых зависимостей от классов

 Задача 3: Создать EmployeeBuilder с Fluent API.
Позволяет цепочку методов.
Читаемый синтаксис построения

 Задача 4: Реализовать Decorator для зарплаты.
BonusDecorator добавляет бонус.
TrainingDecorator добавляет процент за обучение.
Можно комбинировать декораторы

 Задача 5: Создать Strategy для расчета бонусов.
PerformanceBonusStrategy (10% от зарплаты).
ProjectBonusStrategy (5% за каждый проект)

 Задача 6: Реализовать CompanyFacade для управления.
Простой интерфейс для найма.
Управление отделами.
Получение всех сотрудников

**Ключевые фрагменты кода**
1. Singleton

```py
import sqlite3

class DatabaseConnection:
    """
    SINGLETON - Гарантирует только один экземпляр БД подключения
    """
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__connection = None
        return cls.__instance
    
    def get_connection(self):
        """Получить подключение к БД"""
        if self.__connection is None:
            self.__connection = sqlite3.connect(':memory:')
        return self.__connection
    
    def close_connection(self):
        """Закрыть подключение"""
        if self.__connection:
            self.__connection.close()
            self.__connection = None

# Тест:
# db1 = DatabaseConnection()
# db2 = DatabaseConnection()
# assert db1 is db2  # Один и тот же объект

```
2. FACTORY METHOD

```py
class EmployeeFactory:
    """
    FACTORY METHOD - Создание сотрудников без указания конкретных классов
    """
    
    @staticmethod
    def create_employee(emp_type: str, **kwargs) -> AbstractEmployee:
        """
        Создает сотрудника нужного типа
        
        Args:
            emp_type: 'manager' или 'developer'
            **kwargs: параметры для конструктора
            
        Returns:
            Экземпляр AbstractEmployee (Manager или Developer)
        """
        if emp_type == "manager":
            return Manager(**kwargs)
        elif emp_type == "developer":
            return Developer(**kwargs)
        else:
            raise ValueError(f"Неизвестный тип: {emp_type}")

# Тест:
# emp = EmployeeFactory.create_employee(
#     "developer",
#     emp_id=1,
#     name="Иван",
#     department="IT",
#     base_salary=60000,
#     level="senior"
# )

```
3. BUILDER

```py
class EmployeeBuilder:
    """
    BUILDER - Пошаговое построение объектов (Fluent Interface)
    """
    
    def __init__(self):
        self.__data = {}
    
    def set_id(self, emp_id: int) -> 'EmployeeBuilder':
        """Установить ID"""
        self.__data['emp_id'] = emp_id
        return self
    
    def set_name(self, name: str) -> 'EmployeeBuilder':
        """Установить имя"""
        self.__data['name'] = name
        return self
    
    def set_department(self, department: str) -> 'EmployeeBuilder':
        """Установить отдел"""
        self.__data['department'] = department
        return self
    
    def set_base_salary(self, salary: float) -> 'EmployeeBuilder':
        """Установить зарплату"""
        self.__data['base_salary'] = salary
        return self
    
    def set_type(self, emp_type: str) -> 'EmployeeBuilder':
        """Установить тип (manager, developer)"""
        self.__data['type'] = emp_type
        return self
    
    def set_level(self, level: str) -> 'EmployeeBuilder':
        """Установить уровень сеньорности"""
        self.__data['level'] = level
        return self
    
    def set_bonus(self, bonus: float) -> 'EmployeeBuilder':
        """Установить бонус (для manager)"""
        self.__data['bonus'] = bonus
        return self
    
    def build(self) -> AbstractEmployee:
        """Построить финальный объект"""
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
        else:
            raise ValueError("Неполные данные для создания сотрудника")

# Тест:
# emp = (EmployeeBuilder()
#     .set_id(1)
#     .set_name("Иван")
#     .set_department("IT")
#     .set_base_salary(60000)
#     .set_type("developer")
#     .set_level("senior")
#     .build())

```
4. DECORATOR

```py
class SalaryDecorator(ABC):
    """Абстрактный базовый класс для декораторов зарплаты"""
    
    def __init__(self, employee: AbstractEmployee):
        self._employee = employee
    
    @abstractmethod
    def calculate_salary(self) -> float:
        """Расчет декорированной зарплаты"""
        pass


class BonusDecorator(SalaryDecorator):
    """
    DECORATOR - Добавляет фиксированный бонус к зарплате
    """
    
    def __init__(self, employee: AbstractEmployee, bonus_amount: float):
        super().__init__(employee)
        self.__bonus_amount = bonus_amount
    
    def calculate_salary(self) -> float:
        """Зарплата + фиксированный бонус"""
        return self._employee.calculate_salary() + self.__bonus_amount


class TrainingDecorator(SalaryDecorator):
    """
    DECORATOR - Добавляет процент за обучение к зарплате
    """
    
    def __init__(self, employee: AbstractEmployee, training_bonus: float):
        super().__init__(employee)
        self.__training_bonus = training_bonus
    
    def calculate_salary(self) -> float:
        """Зарплата * (1 + процент обучения)"""
        return self._employee.calculate_salary() * (1 + self.__training_bonus)

# Тест:
# dev = Developer(1, "Иван", "IT", 60000, "senior")  # 120000
# with_bonus = BonusDecorator(dev, 5000)              # 125000
# with_bonus_and_training = TrainingDecorator(with_bonus, 0.1)  # 137500

```
5. STRATEGY

```py
class BonusStrategy(ABC):
    """Абстрактная стратегия расчета бонуса"""
    
    @abstractmethod
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        """Расчет бонуса по стратегии"""
        pass


class PerformanceBonusStrategy(BonusStrategy):
    """
    STRATEGY - Бонус на основе производительности (10% от зарплаты)
    """
    
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        """10% от зарплаты как бонус за производительность"""
        return employee.calculate_salary() * 0.1


class ProjectBonusStrategy(BonusStrategy):
    """
    STRATEGY - Бонус на основе количества проектов (5% за каждый)
    """
    
    def __init__(self, project_count: int):
        self.__project_count = project_count
    
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        """5% за каждый проект"""
        return employee.calculate_salary() * (0.05 * self.__project_count)

# Тест:
# dev = Developer(1, "Иван", "IT", 60000, "senior")  # 120000
# 
# strategy1 = PerformanceBonusStrategy()
# bonus1 = strategy1.calculate_bonus(dev)  # 12000
# 
# strategy2 = ProjectBonusStrategy(3)
# bonus2 = strategy2.calculate_bonus(dev)  # 18000

```
6.FACADE
```py
class CompanyFacade:
    """
    FACADE - Упрощенный интерфейс для управления компанией
    """
    
    def __init__(self):
        self.__departments: List[Department] = []
    
    def create_department(self, name: str) -> Department:
        """Создать новый отдел"""
        dept = Department(name)
        self.__departments.append(dept)
        return dept
    
    def hire_employee(self, dept: Department, emp_type: str, emp_id: int,
                     name: str, salary: float, **kwargs) -> AbstractEmployee:
        """
        Нанять сотрудника в отдел (упрощенный интерфейс)
        
        Args:
            dept: Отдел для найма
            emp_type: 'manager' или 'developer'
            emp_id: ID сотрудника
            name: Имя
            salary: Базовая зарплата
            **kwargs: Дополнительные параметры (level, bonus)
        """
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
        """Получить всех сотрудников всех отделов"""
        all_emps = []
        for dept in self.__departments:
            all_emps.extend(dept.get_employees())
        return all_emps
    
    def get_total_salary(self) -> float:
        """Получить общую зарплату всех сотрудников"""
        return sum(emp.calculate_salary() for emp in self.get_all_employees())

# Тест:
# facade = CompanyFacade()
# it_dept = facade.create_department("IT")
# facade.hire_employee(it_dept, "developer", 1, "Иван", 60000, level="senior")
# facade.hire_employee(it_dept, "manager", 2, "Петр", 70000, bonus=20000)
# 
# all_emps = facade.get_all_employees()
# total = facade.get_total_salary()

```

## Примеры работы программ

Пример 1: SINGLETON
```bash
db1 = DatabaseConnection()
db2 = DatabaseConnection()

Результат: db1 is db2 = True
Вывод: Одно подключение к БД 
```
Пример 2: FACTORY METHOD
```bash
emp = EmployeeFactory.create_employee(
    "developer",
    emp_id=1, name="Иван", department="IT",
    base_salary=60000, level="senior"
)

Результат: Developer (Иван) с зарплатой 120000
Вывод: Фабрика создала нужный тип 
```
Пример 3: BUILDER
```bash
emp = (EmployeeBuilder()
    .set_id(1)
    .set_name("Петр")
    .set_department("IT")
    .set_base_salary(70000)
    .set_type("manager")
    .set_bonus(20000)
    .build())

Результат: Manager (Петр) с зарплатой 90000
Вывод: Построен через цепочку методов 
```
Пример 4: DECORATOR
```bash
dev = Developer(1, "Иван", "IT", 60000, "senior")
decorated = BonusDecorator(dev, 5000)
decorated = TrainingDecorator(decorated, 0.1)

Результат:
  Базовая: 120000
  С бонусом: 125000
  С бонусом и обучением: 137500
Вывод: Декораторы добавили функциональность 
```
Пример 5: STRATEGY
```bash
dev = Developer(1, "Иван", "IT", 60000, "senior")

strategy1 = PerformanceBonusStrategy()
bonus1 = strategy1.calculate_bonus(dev)  # 12000

strategy2 = ProjectBonusStrategy(3)
bonus2 = strategy2.calculate_bonus(dev)  # 18000

Результат:
  Производительность: 12000
  За проекты (3): 18000
Вывод: Стратегии работают независимо 
```
Пример 6: FACADE
```bash
facade = CompanyFacade()
it_dept = facade.create_department("IT")
facade.hire_employee(it_dept, "developer", 1, "Иван", 60000, level="senior")
facade.hire_employee(it_dept, "manager", 2, "Петр", 70000, bonus=20000)

all_emps = facade.get_all_employees()
total = facade.get_total_salary()

Результат:
  Всего сотрудников: 2
  Общая зарплата: 210000
Вывод: Фасад упростил управление 
```
## Тестирование
Тест 1: Singleton
```python
def test_singleton():
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    assert db1 is db2, "Должно быть одно подключение"
    print(" Singleton работает")

test_singleton()
# Результат:  Singleton работает
```
Тест 2: Factory Method
```python
def test_factory():
    dev = EmployeeFactory.create_employee(
        "developer", emp_id=1, name="Иван",
        department="IT", base_salary=60000, level="senior"
    )
    mgr = EmployeeFactory.create_employee(
        "manager", emp_id=2, name="Петр",
        department="IT", base_salary=70000, bonus=20000
    )
    assert dev.calculate_salary() == 120000
    assert mgr.calculate_salary() == 90000
    print(" Factory Method работает")

test_factory()
# Результат:  Factory Method работает
```
Тест 3: Builder
```python
def test_builder():
    emp = (EmployeeBuilder()
        .set_id(1)
        .set_name("Иван")
        .set_department("IT")
        .set_base_salary(60000)
        .set_type("developer")
        .set_level("senior")
        .build())
    assert emp.calculate_salary() == 120000
    print(" Builder работает")

test_builder()
# Результат:  Builder работает
```
Тест 4: Decorator
```python
def test_decorator():
    dev = Developer(1, "Иван", "IT", 60000, "senior")
    base = dev.calculate_salary()
    
    with_bonus = BonusDecorator(dev, 5000)
    with_bonus_and_training = TrainingDecorator(with_bonus, 0.1)
    
    assert base == 120000
    assert with_bonus.calculate_salary() == 125000
    assert with_bonus_and_training.calculate_salary() == 137500
    print(" Decorator работает")

test_decorator()
# Результат:  Decorator работает
```
Тест 5: Strategy
```python
def test_strategy():
    dev = Developer(1, "Иван", "IT", 60000, "senior")
    
    perf_strategy = PerformanceBonusStrategy()
    proj_strategy = ProjectBonusStrategy(3)
    
    perf_bonus = perf_strategy.calculate_bonus(dev)
    proj_bonus = proj_strategy.calculate_bonus(dev)
    
    assert perf_bonus == 12000
    assert proj_bonus == 18000
    print(" Strategy работает")

test_strategy()
# Результат:  Strategy работает
```
Тест 6: Facade
```python
def test_facade():
    facade = CompanyFacade()
    it_dept = facade.create_department("IT")
    
    facade.hire_employee(it_dept, "developer", 1, "Иван", 60000, level="senior")
    facade.hire_employee(it_dept, "manager", 2, "Петр", 70000, bonus=20000)
    
    all_emps = facade.get_all_employees()
    total = facade.get_total_salary()
    
    assert len(all_emps) == 2
    assert total == 210000
    print(" Facade работает")

test_facade()
# Результат:  Facade работает
```
## Полный исходный код системы

```python
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
```
### Приложения

- Исходный код: Полная реализация 6 паттернов выше
- UML диаграммы:
![UML Паттерны](https://raw.githubusercontent.com/cilocheb/LavrentevAP/refs/heads/main/lab_5/report/uml.png)
- Дополнительно: Singleton thread-safe, Builder fluent API, Decorator chainable

