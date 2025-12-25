"""Паттерны проектирования"""


class SingletonDatabase:
    """Singleton"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


class EmployeeBuilder:
    """Builder"""

    def __init__(self):
        self._id = None
        self._name = None
        self._department = None
        self._base_salary = None
        self._skills = []
        self._seniority = None
        self._bonus = None

    def set_id(self, emp_id):
        self._id = emp_id
        return self

    def set_name(self, name):
        self._name = name
        return self

    def set_department(self, dept):
        self._department = dept
        return self

    def set_base_salary(self, salary):
        self._base_salary = salary
        return self

    def set_skills(self, skills):
        self._skills = skills
        return self

    def set_seniority(self, level):
        self._seniority = level
        return self

    def set_bonus(self, bonus):
        self._bonus = bonus
        return self

    def build(self):
        from employee import Developer, Manager

        if self._seniority:
            return Developer(
                self._id, self._name, self._department,
                self._base_salary, self._skills, self._seniority
            )
        elif self._bonus is not None:
            return Manager(
                self._id, self._name, self._department,
                self._base_salary, self._bonus
            )


class BonusDecorator:
    """Decorator"""

    def __init__(self, employee, bonus):
        self._employee = employee
        self._bonus = bonus

    def calculate_salary(self):
        return self._employee.calculate_salary() + self._bonus

    def get_info(self):
        return f"{self._employee.get_info()}, бонус: {self._bonus}"


class EmployeeRepository:
    """Repository"""

    def __init__(self):
        self._employees = {}

    def add(self, employee):
        self._employees[employee.id] = employee

    def find_by_id(self, emp_id):
        return self._employees.get(emp_id)

    def get_all(self):
        return list(self._employees.values())
