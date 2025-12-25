import pytest
from employee import Employee, Manager, Developer, Salesperson

@pytest.fixture
def employee():
    return Employee(1, "John Doe", "IT", 5000)

@pytest.fixture
def manager():
    return Manager(1, "Alice", "Management", 7000, 2000)

@pytest.fixture
def developer():
    return Developer(2, "Bob", "DEV", 5000, ["Python"], "senior")

@pytest.fixture
def salesperson():
    return Salesperson(3, "Charlie", "Sales", 4000, 0.15, 50000)
