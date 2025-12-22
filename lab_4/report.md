# **Отчёт по лабораторной работе**
**Тема:** ООП.

## Сведения о студенте

**Дата:** 2025-12-03

**Семестр:** 3

**Группа:** ПИН-б-о-24-1

**Дисциплина:** Технологии программирование

**Студент:** Лаврентьев Аврам Петрович

---

## Оглавление

1. [Введение](#введение)
2. [Структура проекта](#структура-проекта)
3. [Лабораторная работа 4.1: Инкапсуляция](#лабораторная-работа-41-инкапсуляция)
4. [Лабораторная работа 4.2: Наследование и абстракция](#лабораторная-работа-42-наследование-и-абстракция)
5. [Лабораторная работа 4.3: Полиморфизм и магические методы](#лабораторная-работа-43-полиморфизм-и-магические-методы)
6. [Лабораторная работа 4.4: Композиция и агрегация](#лабораторная-работа-44-композиция-и-агрегация)
7. [Выводы](#выводы)
8. [Приложения](#приложения)

---

## Введение

### Цель работы
Разработка комплексной системы учета сотрудников компании с применением принципов объектно-ориентированного программирования.

### Используемые технологии
- **Язык программирования:** Python 3.x
- **Система контроля версий:** Git

---

## Структура проекта

```
lab-03/
├── project/            # Исходный код системы
└── report/             # Всё что нужо для отчёта (например, изображения)
```

---

## Лабораторная работа 4.1: Инкапсуляция

### Цель
Реализация базового класса `Employee` с инкапсуляцией данных и валидацией.

### Выполненные задачи
- Создан класс `Employee` с приватными атрибутами
- Реализованы свойства (property) для доступа к данным
- Добавлена валидация входных параметров
- Реализован метод `__str__` для строкового представления

### Ключевые элементы реализации
```python
class Employee:
    
    
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float):
        self.__id = None
        self.__name = None
        self.__department = None
        self.__base_salary = None
        
   
        self.id = emp_id
        self.name = name
        self.department = department
        self.base_salary = base_salary
    
        # ... остальная реализация

```

### Результаты тестирования
- Протестирована корректная установка и получение значений
- Проверена обработка невалидных данных
- Убедились в корректности строкового представления

---

## Лабораторная работа 4.2: Наследование и абстракция

### Цель
Создание иерархии классов сотрудников на основе наследования и абстракции.

### Выполненные задачи
- Создан абстрактный класс `AbstractEmployee`
- Реализованы классы-наследники: `Manager`, `Developer`, `Salesperson`
- Реализована фабрика сотрудников `EmployeeFactory`
- Переопределены методы расчета зарплат

### Диаграмма классов
![UML](https://raw.githubusercontent.com/cilocheb/LavrentevAP/refs/heads/main/lab_4/report/part2.png)

### Пример использования
```python
=== ИНФОРМАЦИЯ О СОТРУДНИКАХ ===
Обычный сотрудник Иван Иванов: 50000.00 руб.

Менеджер Петр Петров: база=70000.00 + бонус=20000.00 = 90000.00

Разработчик Алексей Сидоров (middle): 90000.00 [Python, Django, PostgreSQL]

Продавец Анна Козлова: ставка=10.0%, продажи=150000, итого=55000.00

=== ЗАРПЛАТЫ ===
Иван Иванов: 50 000 руб.
Петр Петров: 90 000 руб.
Алексей Сидоров: 90 000 руб.
Анна Козлова: 55 000 руб.
Общая зарплата: 285 000 руб.

=== ФАБРИЧНЫЙ МЕТОД ===
Разработчик Мария Петрова (senior): 130 000.00 [JavaScript, Node.js]



```

---

## Лабораторная работа 4.3: Полиморфизм и магические методы

### Цель
Реализация полиморфного поведения и перегрузки операторов.

### Выполненные задачи
- Создан класс `Department` для управления сотрудниками
- Реализованы магические методы для сотрудников и отделов
- Добавлена поддержка сериализации/десериализации
- Реализована итерация по объектам

### Примеры реализации
```python
# Перегрузка операторов для AbstractEmployee
def __eq__(self, other) -> bool:
    """Сравнение сотрудников по ID"""
    if not isinstance(other, AbstractEmployee):
        return NotImplemented
    return self.id == other.id

def __lt__(self, other) -> bool:
    """Сравнение по зарплате (для сортировки)"""
    if not isinstance(other, AbstractEmployee):
        return NotImplemented
    return self.calculate_salary() < other.calculate_salary()

def __add__(self, other) -> float:
    """Сложение двух сотрудников возвращает сумму их зарплат"""
    if not isinstance(other, AbstractEmployee):
        return NotImplemented
    return self.calculate_salary() + other.calculate_salary()

def __radd__(self, other) -> float:
    """Поддержка sum() для списка сотрудников"""
    return self.calculate_salary() + other

AbstractEmployee.__eq__ = __eq__
AbstractEmployee.__lt__ = __lt__
AbstractEmployee.__add__ = __add__
AbstractEmployee.__radd__ = __radd__

# Перегрузка операторов для Department
def __len__(self) -> int:
    """Количество сотрудников в отделе"""
    return len(self.__employees)

def __getitem__(self, index: int) -> AbstractEmployee:
    """Доступ к сотруднику по индексу"""
    return self.__employees[index]

def __contains__(self, employee: AbstractEmployee) -> bool:
    """Проверка принадлежности сотрудника отделу"""
    return employee in self.__employees

def __iter__(self):
    """Итерация по сотрудникам отдела"""
    return iter(self.__employees)

Department.__len__ = __len__
Department.__getitem__ = __getitem__
Department.__contains__ = __contains__
Department.__iter__ = __iter__

# Демонстрация
mgr = Manager(1, "Петр", "IT", 70000, 20000)
dev1 = Developer(2, "Алексей", "IT", 60000, "senior")
dev2 = Developer(3, "Мария", "IT", 50000, "middle")

it_department = Department("IT Отдел")
it_department.add_employee(mgr)
it_department.add_employee(dev1)
it_department.add_employee(dev2)

print("=== ПЕРЕГРУЗКА ОПЕРАТОРОВ ===")

# Операторы для сотрудников
print(f"Сравнение ID: mgr == dev1: {mgr == dev1}")  # False
print(f"Сравнение зарплаты: dev2 < dev1: {dev2 < dev1}")  # True
print(f"Сумма зарплат: dev1 + dev2 = {dev1 + dev2}")  # 160000.0
print(f"sum(it_department) = {sum(it_department)}")  # 270000.0

# Операторы для отдела
print(f"\nКоличество сотрудников: {len(it_department)}")  # 3
print(f"Первый сотрудник: {it_department[0].name}")  # Петр
print(f"dev1 в отделе: {dev1 in it_department}")  # True

# Итерация
print("\nИнформация о всех сотрудниках (полиморфизм):")
for emp in it_department:
    print(f"  - {emp.get_info()}")

```

---

## Лабораторная работа 4.4: Композиция и агрегация

### Цель
Построение сложных объектных структур с использованием композиции и агрегации.

### Выполненные задачи
- Создан класс `Project` с композицией сотрудников
- Реализован класс `Company` с агрегацией отделов и проектов
- Добавлена система валидации и кастомные исключения
- Реализована комплексная сериализация системы

### Примеры реализации
```python
# Композиция: Project содержит команду (композиция)
project_ai = Project(101, "AI Система", "Разработка ИИ", "2026-06-01", "active")
project_web = Project(102, "Веб портал", "Корпоративный сайт", "2026-03-01", "planning")

mgr = Manager(1, "Петр Иванов", "IT", 70000, 20000)
dev = Developer(2, "Алексей Сидоров", "IT", 60000, "senior")

# Добавление команды в проект
project_ai.add_team_member(dev)
project_ai.add_team_member(mgr)

print(f"Проект '{project_ai.name}':")
print(f"  Статус: {project_ai.status}")
print(f"  Команда: {project_ai.team_size} человек")
print(f"  Зарплата команды: {project_ai.calculate_total_salary():,.0f} руб.")

# Агрегация: Company содержит отделы и проекты
company = Company("TechCorp")
it_dept = Department("IT Отдел")
it_dept.add_employee(mgr)
it_dept.add_employee(dev)

company.add_department(it_dept)
company.add_project(project_ai)
company.add_project(project_web)

print(f"\nКомпания '{company.name}':")
print(f"  Отделов: {len(company.__departments)}")
print(f"  Проектов: {len(company.__projects)}")
print(f"  Всего сотрудников: {len(company.get_all_employees())}")
print(f"  Месячные затраты: {company.calculate_total_monthly_cost():,.0f} руб.")

# Валидация статусов
try:
    project_ai.status = "invalid_status"
except ValueError as e:
    print(f"✓ Валидация работает: {e}")

# Поиск сотрудника
found_emp = company.find_employee_by_id(1)
print(f"\nПоиск сотрудника ID=1: {found_emp.name if found_emp else 'Не найден'}")

# Экспорт данных
company.export_employees_csv("сотрудники.csv")
company.save_to_json("компания.json")
print("\nЭкспортировано:")
print("  - сотрудники.csv")
print("  - компания.json")

# Фильтрация проектов
active_projects = company.get_projects_by_status("active")
print(f"\nАктивные проекты ({len(active_projects)}):")
for proj in active_projects:
    print(f"  - {proj.name}")

```

---

## Выводы
1. **ООП делает код гибким и понятным** - абстракция и наследование помогают создавать иерархии объектов (сотрудники разных типов), композиция и агрегация управляют связями между ними (отделы, проекты).
2. **Паттерны решают типовые проблемы** - фабрика создает объекты, исключения обрабатывают ошибки, полиморфизм позволяет работать с разными объектами одинаково.
3. **Хорошая архитектура экономит время** - система с сериализацией, валидацией и отчетами из учебного примера становится готовым решением для реального учета сотрудников в компании.
---

## Приложения

### Приложение A: UML-диаграммы классов
![UML](https://raw.githubusercontent.com/cilocheb/LavrentevAP/refs/heads/main/lab_4/report/part2.png)

---

## Список использованных источников

1. Роберт Мартин. "Чистый код. Создание, анализ и рефакторинг"
2. Мартин Фаулер. "Рефакторинг. Улучшение существующего кода"
3. Эрик Гамма и др. "Паттерны объектно-ориентированного проектирования"
4. Документация Python: https://docs.python.org/3/
5. Документация pytest: https://docs.pytest.org/

