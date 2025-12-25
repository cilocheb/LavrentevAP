"""Классы сотрудников"""


class Employee:
    """Базовый класс сотрудника"""

    def __init__(self, emp_id, name, department, base_salary):
        if emp_id <= 0:
            raise ValueError("ID должен быть положительным числом")
        if not name or name == "":
            raise ValueError("Имя не может быть пустым")
        if base_salary < 0:
            raise ValueError("Зарплата не может быть отрицательной")

        self._id = emp_id
        self._name = name
        self._department = department
        self._base_salary = base_salary

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Имя не может быть пустым")
        self._name = value

    @property
    def base_salary(self):
        return self._base_salary

    @base_salary.setter
    def base_salary(self, value):
        if value < 0:
            raise ValueError("Зарплата не может быть отрицательной")
        self._base_salary = value

    @property
    def department(self):
        return self._department

    def calculate_salary(self):
        return self._base_salary

    def __str__(self):
        return f"Сотрудник [id: {self.id}, имя: {self.name}, отдел: {self.department}, базовая зарплата: {self.base_salary}]"

    def get_info(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Employee):
            return self.id == other.id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, Employee):
            return self.calculate_salary() < other.calculate_salary()
        return False

    def __gt__(self, other):
        if isinstance(other, Employee):
            return self.calculate_salary() > other.calculate_salary()
        return False

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    def __add__(self, other):
        if isinstance(other, Employee):
            return self.calculate_salary() + other.calculate_salary()
        return NotImplemented


class Manager(Employee):
    """Менеджер"""

    def __init__(self, emp_id, name, department, base_salary, bonus):
        super().__init__(emp_id, name, department, base_salary)

        if bonus < 0:
            raise ValueError("Бонус не может быть отрицательным")

        self._bonus = bonus

    @property
    def bonus(self):
        return self._bonus

    @bonus.setter
    def bonus(self, value):
        if value < 0:
            raise ValueError("Бонус не может быть отрицательным")
        self._bonus = value

    def calculate_salary(self):
        return self._base_salary + self._bonus

    def get_info(self):
        return f"Менеджер: {self.name}, зарплата: {self.calculate_salary()}, бонус: {self.bonus}, итоговая зарплата: {self.calculate_salary()}"


class Developer(Employee):
    """Разработчик"""

    SENIORITY_MULTIPLIERS = {
        "junior": 1.0,
        "middle": 1.5,
        "senior": 2.0
    }

    def __init__(self, emp_id, name, department, base_salary, skills, seniority_level):
        super().__init__(emp_id, name, department, base_salary)
        self._skills = skills if isinstance(skills, list) else [skills]

        if seniority_level not in self.SENIORITY_MULTIPLIERS:
            raise ValueError(f"Неверный уровень: {seniority_level}")

        self._seniority_level = seniority_level

    @property
    def skills(self):
        return self._skills

    @property
    def seniority_level(self):
        return self._seniority_level

    def add_skill(self, skill):
        if skill not in self._skills:
            self._skills.append(skill)

    def calculate_salary(self):
        multiplier = self.SENIORITY_MULTIPLIERS[self._seniority_level]
        return int(self._base_salary * multiplier)

    def get_info(self):
        skills_str = ", ".join(self._skills)
        return f"Разработчик: {self.name}, уровень: {self._seniority_level}, навыки: {skills_str}, зарплата: {self.calculate_salary()}"

    def __iter__(self):
        return iter(self._skills)


class Salesperson(Employee):
    """Менеджер по продажам"""

    def __init__(self, emp_id, name, department, base_salary, commission_rate, sales_volume):
        super().__init__(emp_id, name, department, base_salary)
        self._commission_rate = commission_rate
        self._sales_volume = sales_volume

    @property
    def commission_rate(self):
        return self._commission_rate

    @property
    def sales_volume(self):
        return self._sales_volume

    def update_sales(self, new_volume):
        self._sales_volume = new_volume

    def calculate_salary(self):
        return int(self._base_salary + (self._sales_volume * self._commission_rate))

    def get_info(self):
        commission = self._sales_volume * self._commission_rate
        return f"Менеджер по продажам: {self.name}, комиссия: {self.commission_rate}, объем продаж: {self._sales_volume}, доход: {commission}, зарплата: {self.calculate_salary()}"


class EmployeeFactory:
    """Factory для создания сотрудников"""

    @staticmethod
    def create_employee(emp_type, **kwargs):
        if emp_type == "manager":
            return Manager(
                kwargs["id"],
                kwargs["name"],
                kwargs["department"],
                kwargs["base_salary"],
                kwargs.get("bonus", 0)
            )
        elif emp_type == "developer":
            return Developer(
                kwargs["id"],
                kwargs["name"],
                kwargs["department"],
                kwargs["base_salary"],
                kwargs.get("skills", []),
                kwargs.get("seniority_level", "junior")
            )
        elif emp_type == "salesperson":
            return Salesperson(
                kwargs["id"],
                kwargs["name"],
                kwargs["department"],
                kwargs["base_salary"],
                kwargs.get("commission_rate", 0),
                kwargs.get("sales_volume", 0)
            )
        else:
            raise ValueError(f"Неизвестный тип: {emp_type}")
