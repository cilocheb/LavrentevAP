from abc import ABC, abstractmethod
from typing import List, Optional
import json

class Employee:
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float):
        self.__id = emp_id
        self.__name = name
        self.__department = department
        self.__base_salary = base_salary
    
    @property
    def id(self) -> int: 
        return self.__id
    
    @property
    def name(self) -> str: 
        return self.__name
    
    @property
    def base_salary(self) -> float:
        return self.__base_salary

class AbstractEmployee(Employee, ABC):
    @abstractmethod
    def calculate_salary(self) -> float: pass

class Manager(AbstractEmployee):
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float, bonus: float):
        super().__init__(emp_id, name, department, base_salary)
        self.__bonus = bonus
    
    def calculate_salary(self) -> float:
        return self.base_salary + self.__bonus

class Developer(AbstractEmployee):
    SENIORITY = {"junior": 1.0, "middle": 1.5, "senior": 2.0}
    
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float, level: str):
        super().__init__(emp_id, name, department, base_salary)
        self.__level = level
    
    def calculate_salary(self) -> float:
        return self.base_salary * self.SENIORITY[self.__level]

class Department:
    def __init__(self, name: str):
        self.name = name
        self.__employees: List[AbstractEmployee] = []
    
    def add_employee(self, employee: AbstractEmployee) -> None:
        self.__employees.append(employee)
    
    def remove_employee(self, emp_id: int) -> None:
        self.__employees = [e for e in self.__employees if e.id != emp_id]
    
    def get_employees(self) -> List[AbstractEmployee]:
        return self.__employees[:]
    
    def calculate_total_salary(self) -> float:
        return sum(emp.calculate_salary() for emp in self.__employees)
    
    def find_employee_by_id(self, emp_id: int) -> Optional[AbstractEmployee]:
        for emp in self.__employees:
            if emp.id == emp_id:
                return emp
        return None
    
    def __len__(self) -> int:
        return len(self.__employees)
    
    def __getitem__(self, index: int) -> AbstractEmployee:
        return self.__employees[index]
    
    def __contains__(self, employee: AbstractEmployee) -> bool:
        return employee in self.__employees
    
    def __iter__(self):
        return iter(self.__employees)
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "employees": [
                {
                    "type": type(emp).__name__,
                    "id": emp.id,
                    "name": emp.name,
                    "salary": emp.calculate_salary()
                }
                for emp in self.__employees
            ]
        }
    
    def save_to_file(self, filename: str) -> None:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

def make_eq(self, other):
    return self.id == other.id if isinstance(other, AbstractEmployee) else False
AbstractEmployee.__eq__ = make_eq

def make_lt(self, other):
    return self.calculate_salary() < other.calculate_salary() if isinstance(other, AbstractEmployee) else False
AbstractEmployee.__lt__ = make_lt

def make_add(self, other):
    return self.calculate_salary() + other.calculate_salary() if isinstance(other, AbstractEmployee) else NotImplemented
AbstractEmployee.__add__ = make_add

def make_radd(self, other):
    return other + self.calculate_salary()
AbstractEmployee.__radd__ = make_radd

if __name__ == "__main__":
    dept = Department("IT Отдел")
    
    mgr = Manager(1, "Петр", "IT", 70000, 20000)
    dev1 = Developer(2, "Алексей", "IT", 60000, "senior")
    dev2 = Developer(3, "Мария", "IT", 50000, "middle")
    
    dept.add_employee(mgr)
    dept.add_employee(dev1)
    dept.add_employee(dev2)
    
    print(f"Отдел: {dept.name} ({len(dept)} сотрудников)")
    print(f"Общая зарплата: {dept.calculate_total_salary():,.0f}")
    
    print("\nСотрудники:")
    for i, emp in enumerate(dept):
        print(f"{i+1}. {emp.name}: {emp.calculate_salary():,.0f}")
    
    print(f"\nПоиск ID=2: {dept.find_employee_by_id(2).name if dept.find_employee_by_id(2) else 'Не найден'}")
    
    print("\nОператоры:")
    print(f"dev1 в отделе: {dev1 in dept}")
    print(f"Первый сотрудник: {dept[0].name}")
    print(f"dev1 < mgr: {dev1 < mgr}")
    print(f"dev1 + dev2: {dev1 + dev2}")
    print(f"sum(dept): {sum(dept):,.0f}")
    
    print("\nСериализация:")
    dept.save_to_file("dept.json")
    print("Сохранено в dept.json")

