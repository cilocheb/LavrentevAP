
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
import json
import csv


class Employee:
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float):
        self.__id = emp_id
        self.__name = name
        self.__department = department
        self.__base_salary = base_salary
    
    @property
    def id(self) -> int: return self.__id
    @property
    def name(self) -> str: return self.__name
    @property
    def base_salary(self) -> float: return self.__base_salary

class AbstractEmployee(Employee, ABC):
    @abstractmethod
    def calculate_salary(self) -> float: pass

class Manager(AbstractEmployee):
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float, bonus: float):
        super().__init__(emp_id, name, department, base_salary)
        self.__bonus = bonus
    def calculate_salary(self) -> float: return self.base_salary + self.__bonus

class Developer(AbstractEmployee):
    SENIORITY = {"junior": 1.0, "middle": 1.5, "senior": 2.0}
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float, level: str):
        super().__init__(emp_id, name, department, base_salary)
        self.__level = level
    def calculate_salary(self) -> float: return self.base_salary * self.SENIORITY[self.__level]

class Department:
    def __init__(self, name: str):
        self.name = name
        self.__employees: List[AbstractEmployee] = []
    
    def add_employee(self, employee: AbstractEmployee) -> None:
        self.__employees.append(employee)
    
    def get_employees(self) -> List[AbstractEmployee]:
        return self.__employees[:]
    
    def calculate_total_salary(self) -> float:
        return sum(emp.calculate_salary() for emp in self.__employees)


class Project:
    VALID_STATUSES = ["planning", "active", "completed", "cancelled"]
    
    def __init__(self, project_id: int, name: str, description: str, deadline: str, status: str):
        self.__project_id = project_id
        self.name = name
        self.description = description
        self.deadline = deadline
        self.__status = status
        self.__team: List[AbstractEmployee] = []
    
    @property
    def project_id(self) -> int: return self.__project_id
    
    @property
    def status(self) -> str: return self.__status
    
    @status.setter
    def status(self, value: str) -> None:
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Статус должен быть: {self.VALID_STATUSES}")
        self.__status = value
    
    @property
    def team_size(self) -> int:
        return len(self.__team)
    
    def add_team_member(self, employee: AbstractEmployee) -> None:
        self.__team.append(employee)
    
    def remove_team_member(self, emp_id: int) -> None:
        self.__team = [e for e in self.__team if e.id != emp_id]
    
    def calculate_total_salary(self) -> float:
        return sum(emp.calculate_salary() for emp in self.__team)
    
    def get_team(self) -> List[AbstractEmployee]:
        return self.__team[:]

class Company:
    def __init__(self, name: str):
        self.name = name
        self.__departments: List[Department] = []
        self.__projects: List[Project] = []
    
    def add_department(self, department: Department) -> None:
        self.__departments.append(department)
    
    def add_project(self, project: Project) -> None:
        self.__projects.append(project)
    
    def get_all_employees(self) -> List[AbstractEmployee]:
        employees = []
        for dept in self.__departments:
            employees.extend(dept.get_employees())
        return employees
    
    def find_employee_by_id(self, emp_id: int) -> Optional[AbstractEmployee]:
        for dept in self.__departments:
            for emp in dept.get_employees():
                if emp.id == emp_id:
                    return emp
        return None
    
    def calculate_total_monthly_cost(self) -> float:
        total = 0
        for dept in self.__departments:
            total += dept.calculate_total_salary()
        for proj in self.__projects:
            total += proj.calculate_total_salary()
        return total
    
    def get_projects_by_status(self, status: str) -> List[Project]:
        return [p for p in self.__projects if p.status == status]
    
    def export_employees_csv(self, filename: str) -> None:
        employees = self.get_all_employees()
        if employees:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Имя', 'Отдел', 'Зарплата'])
                for emp in employees:
                    writer.writerow([emp.id, emp.name, emp.department, emp.calculate_salary()])
    
    def save_to_json(self, filename: str) -> None:
        data = {
            "name": self.name,
            "departments": [{"name": d.name, "employee_count": len(d.get_employees())} for d in self.__departments],
            "projects": [{"id": p.project_id, "name": p.name, "status": p.status} for p in self.__projects],
            "total_cost": self.calculate_total_monthly_cost()
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    company = Company("TechCorp")
    
   
    it_dept = Department("IT")
    sales_dept = Department("Продажи")
    
    mgr = Manager(1, "Петр", "IT", 70000, 20000)
    dev = Developer(2, "Алексей", "IT", 60000, "senior")
    sales_person = Developer(3, "Анна", "Продажи", 40000, "middle")
    
    it_dept.add_employee(mgr)
    it_dept.add_employee(dev)
    sales_dept.add_employee(sales_person)
    
    company.add_department(it_dept)
    company.add_department(sales_dept)
    

    project2 = Project(102, "Веб портал", "Корпоративный сайт", "2026-03-01", "planning")
    
    project1.add_team_member(dev)
    project1.add_team_member(mgr)
    company.add_project(project1)
    company.add_project(project2)
    
    print(f"Компания: {company.name}")
    print(f"Всего сотрудников: {len(company.get_all_employees())}")
    print(f"Общие месячные затраты: {company.calculate_total_monthly_cost():,.0f}")
    
    print("\nПроекты по статусу 'active':")
    active_projects = company.get_projects_by_status("active")
    for proj in active_projects:
        print(f"  - {proj.name} (команда: {proj.team_size})")
    
    print("\nЭкспорт:")
    company.export_employees_csv("employees.csv")
    company.save_to_json("company.json")
    print("Сохранено: employees.csv, company.json")
