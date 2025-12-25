"""Класс проекта"""


class Project:
    """Проект с командой"""

    VALID_STATUSES = ["planning", "in_progress", "completed"]

    def __init__(self, proj_id, name, description, deadline, status):
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")

        self.id = proj_id
        self.name = name
        self.description = description
        self.deadline = deadline
        self.status = status
        self._team = []

    def add_team_member(self, employee):
        self._team.append(employee)

    def remove_team_member(self, emp_id):
        self._team = [e for e in self._team if e.id != emp_id]

    def get_team(self):
        return self._team

    def get_team_size(self):
        return len(self._team)

    def calculate_total_salary(self):
        return sum(emp.calculate_salary() for emp in self._team)
