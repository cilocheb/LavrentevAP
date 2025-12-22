from abc import ABC, abstractmethod
from typing import List

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
        return f"Сотрудник [id:{self.id}, {self.name}, {self.department}, {self.base_salary}]"

class AbstractEmployee(Employee, ABC):
    @abstractmethod
    def calculate_salary(self) -> float:
        pass
    
    @abstractmethod
    def get_info(self) -> str:
        pass

class RegularEmployee(AbstractEmployee):
    def calculate_salary(self) -> float:
        return self.base_salary
    
    def get_info(self) -> str:
        return f"Обычный сотрудник {self.name}: {self.calculate_salary():.2f} руб."

class Manager(AbstractEmployee):
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float, bonus: float):
        super().__init__(emp_id, name, department, base_salary)
        self.__bonus = bonus
    
    @property
    def bonus(self) -> float:
        return self.__bonus
    @bonus.setter
    def bonus(self, value: float) -> None:
        if value < 0:
            raise ValueError("Бонус неотрицательный")
        self.__bonus = value
    
    def calculate_salary(self) -> float:
        return self.base_salary + self.bonus
    
    def get_info(self) -> str:
        return f"Менеджер {self.name}: база={self.base_salary:.2f} + бонус={self.bonus:.2f} = {self.calculate_salary():.2f}"

class Developer(AbstractEmployee):
    SENIORITY = {"junior": 1.0, "middle": 1.5, "senior": 2.0}
    
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float, tech_stack: List[str], level: str):
        super().__init__(emp_id, name, department, base_salary)
        self.__tech_stack = tech_stack
        self.__level = level
    
    @property
    def tech_stack(self) -> List[str]:
        return self.__tech_stack
    
    @property
    def level(self) -> str:
        return self.__level
    
    def calculate_salary(self) -> float:
        return self.base_salary * self.SENIORITY[self.level]
    
    def get_info(self) -> str:
        return f"Разработчик {self.name} ({self.level}): {self.calculate_salary():.2f} [{', '.join(self.tech_stack)}]"

class Salesperson(AbstractEmployee):
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float, rate: float, sales: float):
        super().__init__(emp_id, name, department, base_salary)
        self.__rate = rate
        self.__sales = sales
    
    @property
    def rate(self) -> float:
        return self.__rate
    
    @property
    def sales(self) -> float:
        return self.__sales
    
    def update_sales(self, amount: float) -> None:
        self.__sales += amount
    
    def calculate_salary(self) -> float:
        return self.base_salary + self.sales * self.rate
    
    def get_info(self) -> str:
        return f"Продавец {self.name}: ставка={self.rate:.1%}, продажи={self.sales:.0f}, итого={self.calculate_salary():.2f}"

class EmployeeFactory:
    @staticmethod
    def create_employee(emp_type: str, **kwargs) -> AbstractEmployee:
        types = {"employee": RegularEmployee, "manager": Manager, "developer": Developer, "salesperson": Salesperson}
        if emp_type.lower() not in types:
            raise ValueError("Неизвестный тип")
        return types[emp_type.lower()](**kwargs)

if __name__ == "__main__":
    emp1 = RegularEmployee(1, "Иван", "IT", 5000)
    mgr = Manager(2, "Анна", "HR", 7000, 2000)
    dev = Developer(3, "Михаил", "Dev", 6000, ["Python"], "senior")
    sales = Salesperson(4, "Елена", "Sales", 4000, 0.15, 50000)
    
    employees = [emp1, mgr, dev, sales]
    
    for emp in employees:
        print(emp.get_info())
    
    factory_dev = EmployeeFactory.create_employee("developer", emp_id=5, name="Олег", department="Dev", base_salary=5500, tech_stack=["Docker"], level="middle")
    print(factory_dev.get_info())

if __name__ == "__main__":
    # Создание сотрудников разных типов
    employee = RegularEmployee(1, "Иван Иванов", "Бухгалтерия", 50000)
    manager = Manager(2, "Петр Петров", "Менеджмент", 70000, 20000)
    developer = Developer(3, "Алексей Сидоров", "IT", 60000, ["Python", "Django", "PostgreSQL"], "middle")
    salesperson = Salesperson(4, "Анна Козлова", "Продажи", 40000, 0.1, 150000)
    
    # Список всех сотрудников (полиморфизм)
    employees = [employee, manager, developer, salesperson]
    
    print("=== ИНФОРМАЦИЯ О СОТРУДНИКАХ ===")
    for emp in employees:
        print(emp.get_info())
        print()
    
    print("=== ЗАРПЛАТЫ ===")
    total_salary = sum(emp.calculate_salary() for emp in employees)
    for emp in employees:
        print(f"{emp.name}: {emp.calculate_salary():,.0f} руб.")
    print(f"Общая зарплата: {total_salary:,.0f} руб.")
    
    print("\n=== ФАБРИЧНЫЙ МЕТОД ===")
    factory_dev = EmployeeFactory.create_employee(
        "developer", 
        emp_id=5, 
        name="Мария Петрова", 
        department="Backend", 
        base_salary=65000, 
        tech_stack=["JavaScript", "Node.js"], 
        level="senior"
    )
    print(factory_dev.get_info())
    

