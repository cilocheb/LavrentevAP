"""Валидация данных сотрудников."""


class EmployeeValidator:
    """Валидатор для данных сотрудников."""

    @staticmethod
    def validate_id(emp_id: int) -> None:
        """Проверка ID сотрудника.

        Args:
            emp_id: Идентификатор сотрудника

        Raises:
            ValueError: Если ID <= 0
        """
        if emp_id <= 0:
            raise ValueError("ID должен быть положительным числом")

    @staticmethod
    def validate_name(name: str) -> None:
        """Проверка имени сотрудника.

        Args:
            name: Имя сотрудника

        Raises:
            ValueError: Если имя пусто или не строка
        """
        if not name or not isinstance(name, str):
            raise ValueError("Имя должно быть непустой строкой")

    @staticmethod
    def validate_salary(salary: float) -> None:
        """Проверка зарплаты.

        Args:
            salary: Размер зарплаты

        Raises:
            ValueError: Если зарплата < 0
        """
        if salary < 0:
            raise ValueError("Зарплата не может быть отрицательной")

    @staticmethod
    def validate_employee(emp_id: int, name: str, salary: float) -> None:
        """Полная валидация данных сотрудника.

        Args:
            emp_id: Идентификатор
            name: Имя
            salary: Зарплата

        Raises:
            ValueError: Если что-то неправильно
        """
        EmployeeValidator.validate_id(emp_id)
        EmployeeValidator.validate_name(name)
        EmployeeValidator.validate_salary(salary)
