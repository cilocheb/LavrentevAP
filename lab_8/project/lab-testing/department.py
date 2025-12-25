"""Класс отдела"""


class Department:
    """Отдел с сотрудниками"""

    def __init__(self, name):
        self.name = name
        self._employees = []

    def add_employee(self, employee):
        self._employees.append(employee)

    def remove_employee(self, emp_id):
        self._employees = [e for e in self._employees if e.id != emp_id]

    def get_employees(self):
        return self._employees

    def calculate_total_salary(self):
        return sum(emp.calculate_salary() for emp in self._employees)

    def __len__(self):
        return len(self._employees)

    def __getitem__(self, index):
        return self._employees[index]

    def __contains__(self, employee):
        return employee in self._employees

    def __iter__(self):
        return iter(self._employees)
