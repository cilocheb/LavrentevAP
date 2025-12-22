class Employee:
    
    
    def __init__(self, emp_id: int, name: str, department: str, base_salary: float):
        """
        Инициализация объекта Employee.
        
        Args:
            emp_id: Уникальный идентификатор сотрудника (должен быть > 0)
            name: Имя сотрудника (не должно быть пустым)
            department: Отдел (не должно быть пустым)
            base_salary: Базовая зарплата (должна быть > 0)
        
        Raises:
            ValueError: Если переданы невалидные данные
        """
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
        if not isinstance(value, int):
            raise ValueError(f"ID должен быть целым числом, получено: {type(value).__name__}")
        if value <= 0:
            raise ValueError(f"ID должен быть положительным числом, получено: {value}")
        self.__id = value
    
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError(f"Имя должно быть строкой, получено: {type(value).__name__}")
        if not value.strip():
            raise ValueError("Имя не должно быть пустым")
        self.__name = value.strip()
    
   
    @property
    def department(self) -> str:
        return self.__department
    
    @department.setter
    def department(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError(f"Отдел должен быть строкой, получено: {type(value).__name__}")
        if not value.strip():
            raise ValueError("Отдел не должен быть пустым")
        self.__department = value.strip()
    
   
    @property
    def base_salary(self) -> float:
        return self.__base_salary
    
    @base_salary.setter
    def base_salary(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise ValueError(f"Зарплата должна быть числом, получено: {type(value).__name__}")
        if value <= 0:
            raise ValueError(f"Зарплата должна быть положительной, получено: {value}")
        self.__base_salary = float(value)
    
    def __str__(self) -> str:
        return (f"Сотрудник [id: {self.__id}, имя: {self.__name}, "
                f"отдел: {self.__department}, базовая зарплата: {self.__base_salary}]")

#Тесты

    
    # Тест 1: Создание корректных объектов
    print("\n Тест 1: Создание корректных объектов")
    print("-" * 60)
    
    try:
        emp1 = Employee(1, "Иван Петров", "IT", 5000)
        print(f"✓ emp1: {emp1}")
        
        emp2 = Employee(2, "Мария Сидорова", "HR", 4500)
        print(f"✓ emp2: {emp2}")
        
        emp3 = Employee(3, "Петр Иванов", "Sales", 4000)
        print(f"✓ emp3: {emp3}")
    except ValueError as e:
        print(f"✗ Ошибка: {e}")
    
    # Тест 2: Получение значений через свойства
    print("\n Тест 2: Получение значений через геттеры")
    print("-" * 60)
    print(f"ID: {emp1.id}")
    print(f"Имя: {emp1.name}")
    print(f"Отдел: {emp1.department}")
    print(f"Базовая зарплата: {emp1.base_salary}")
    
    # Тест 3: Изменение значений через сеттеры
    print("\n Тест 3: Изменение значений через сеттеры")
    print("-" * 60)
    
    try:
        emp1.base_salary = 6000
        print(f" Зарплата увеличена до {emp1.base_salary}")
        
        emp1.department = "Development"
        print(f" Отдел изменен на '{emp1.department}'")
        
        print(f"\nОбновленный объект: {emp1}")
    except ValueError as e:
        print(f" Ошибка: {e}")
    
    # Тест 4: Попытка установки невалидных значений
    print("\n Тест 4: Попытка установки невалидных значений (должны вызвать исключения)")
    print("-" * 60)
    
    # Попытка установить отрицательный ID
    print("\n1️ Попытка установить отрицательный ID:")
    try:
        emp2.id = -5
        print(" Ошибка: исключение не было вызвано!")
    except ValueError as e:
        print(f" Перехвачена ошибка: {e}")
    
    # Попытка установить пустое имя
    print("\n2️ Попытка установить пустое имя:")
    try:
        emp2.name = ""
        print(" Ошибка: исключение не было вызвано!")
    except ValueError as e:
        print(f" Перехвачена ошибка: {e}")
    
    # Попытка установить отрицательную зарплату
    print("\n3 Попытка установить отрицательную зарплату:")
    try:
        emp3.base_salary = -3000
        print("Ошибка: исключение не было вызвано!")
    except ValueError as e:
        print(f"Перехвачена ошибка: {e}")
    
    # Попытка установить зарплату как строку
    print("\n4️ Попытка установить зарплату как строку:")
    try:
        emp1.base_salary = "много денег"
        print("Ошибка: исключение не было вызвано!")
    except ValueError as e:
        print(f"Перехвачена ошибка: {e}")
    
    # Попытка установить пустой отдел
    print("\n5 Попытка установить пустой отдел:")
    try:
        emp3.department = "   "
        print(" Ошибка: исключение не было вызвано!")
    except ValueError as e:
        print(f" Перехвачена ошибка: {e}")
    
    # Тест 5: Создание объекта с невалидными параметрами в конструкторе
    print("\n Тест 5: Создание с невалидными параметрами в конструкторе")
    print("-" * 60)
    
    print("\n1⃣ Попытка создать сотрудника с ID = 0:")
    try:
        emp_bad = Employee(0, "Тест", "IT", 5000)
    except ValueError as e:
        print(f" Перехвачена ошибка: {e}")
    
    print("\n2️ Попытка создать сотрудника с нулевой зарплатой:")
    try:
        emp_bad = Employee(10, "Тест", "IT", 0)
    except ValueError as e:
        print(f" Перехвачена ошибка: {e}")
    
    print("\n3 Попытка создать сотрудника с пустым именем:")
    try:
        emp_bad = Employee(10, "", "IT", 5000)
    except ValueError as e:
        print(f" Перехвачена ошибка: {e}")
    
