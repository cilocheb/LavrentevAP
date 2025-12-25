"""Класс компании"""

from department import Department


class Company:
    """Компания с отделами"""

    def __init__(self, name):
        self.name = name
        self._departments = []

    def add_department(self, department):
        self._departments.append(department)

    def remove_department(self, dept_name):
        dept = self.find_department(dept_name)
        if dept and len(dept) > 0:
            raise ValueError("Cannot delete department with employees")
        self._departments = [d for d in self._departments if d.name != dept_name]

    def find_department(self, dept_name):
        for dept in self._departments:
            if dept.name == dept_name:
                return dept
        return None

    def find_employee_by_id(self, emp_id):
        for dept in self._departments:
            for emp in dept:
                if emp.id == emp_id:
                    return emp
        return None

    def get_departments(self):
        return self._departments

    def get_all_employees(self):
        all_emps = []
        for dept in self._departments:
            all_emps.extend(list(dept))
        return all_emps

    def calculate_total_monthly_cost(self):
        total = 0
        for dept in self._departments:
            total += dept.calculate_total_salary()
        return total
