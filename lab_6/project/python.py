

# 1. ФУНКЦИИ КАК ОБЪЕКТЫ ПЕРВЫГО КЛАССА


def square(x):
    """Простая функция"""
    return x * x

def cube(x):
    """Функция куба"""
    return x * x * x

def apply_function(func, value):
    """Применяет функцию к значению"""
    return func(value)

def create_multiplier(factor):
    """Создаёт множитель (замыкание)"""
    def multiplier(x):
        return x * factor
    return multiplier


# 2. LAMBDA-ФУНКЦИИ И ЗАКРЫТИЯ


numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Lambda для квадратов
squares = list(map(lambda x: x*x, numbers))

# Lambda для чётных чисел
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))

# Сложная lambda
complex_operation = lambda x: x**2 + 2*x + 1

# Замыкание-счётчик
def create_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter


# 3. ФУНКЦИИ ВЫСШЕГО ПОРЯДКА (map/filter/reduce)


from functools import reduce

students = [
    {"name": "Alice", "grade": 85, "age": 20},
    {"name": "Bob", "grade": 92, "age": 22},
    {"name": "Charlie", "grade": 78, "age": 19},
    {"name": "Diana", "grade": 95, "age": 21},
    {"name": "Eve", "grade": 88, "age": 20}
]

# map - имена студентов
student_names = list(map(lambda student: student["name"], students))

# filter - отличники (grade >= 90)
top_students = list(filter(lambda student: student["grade"] >= 90, students))

# reduce - произведение чисел 1-10
product = reduce(lambda x, y: x * y, numbers)

# Комплексная обработка
def process_student_data(students):
    result = list(
        map(lambda s: {
            "name": s["name"].upper(),
            "status": "Excellent" if s["grade"] >= 90 else "Good"
        }, 
        filter(lambda s: s["grade"] >= 80, students)
        )
    )
    return result

processed_data = process_student_data(students)


# 4. LIST COMPREHENSIONS И ГЕНЕРАТОРЫ


# List comprehensions
squares_lc = [x*x for x in numbers]
even_squares = [x*x for x in numbers if x % 2 == 0]
student_dict = {student["name"]: student["grade"] for student in students}
unique_ages = {student["age"] for student in students}

# Генератор Фибоначчи
def fibonacci_generator(limit):
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1

# Генератор квадратов
squares_gen = (x*x for x in numbers)


# 5. ДЕКОРАТОРЫ


import time
from functools import wraps

def timer(func):
    """Измеряет время выполнения"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__}: {end_time - start_time:.4f} сек")
        return result
    return wrapper

def repeat(num_times):
    """Повторяет функцию"""
    def decorator_repeat(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_repeat

@timer
@repeat(3)
def slow_function():
    time.sleep(0.5)
    return "Готово!"

@timer
def expensive_operation(x):
    print(f"Вычисляю {x}...")
    time.sleep(0.5)
    return x * x

# Кэширующий декоратор
def cache(func):
    cached_results = {}
    @wraps(func)
    def wrapper(*args):
        if args in cached_results:
            print(f"Из кэша: {args}")
            return cached_results[args]
        result = func(*args)
        cached_results[args] = result
        return result
    return wrapper

@cache
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


# 6. ПРАКТИЧЕСКИЕ ЗАДАНИЯ


# ЗАДАНИЕ 1: Анализ студентов (map/filter/reduce)
def analyze_students(students):
    # Отличники (grade >= 90)
    excellent = list(filter(lambda s: s["grade"] >= 90, students))
    # Проходные (grade >= 60)
    passed = list(filter(lambda s: s["grade"] >= 60, students))
    # Средний балл
    avg_grade = reduce(lambda x, y: x + y["grade"], students, 0) / len(students)
    return {
        "excellent_count": len(excellent),
        "passed_count": len(passed),
        "average_grade": avg_grade
    }

# ЗАДАНИЕ 2: Логгер (декоратор)
def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Вызов {func.__name__} с аргументами {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"Результат: {result}")
        return result
    return wrapper

@logger
def multiply(a, b):
    return a * b

# ЗАДАНИЕ 3: Генератор простых чисел
def prime_generator(limit):
    """Генератор простых чисел до limit"""
    yield 2
    primes = [2]
    for num in range(3, limit + 1, 2):
        is_prime = True
        for prime in primes:
            if prime * prime > num:
                break
            if num % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
            yield num


# 7. MAIN - ДЕМОНСТРАЦИЯ ВСЕГО

def main():
    print(" ЛАБОРАТОРНАЯ РАБОТА №6: PYTHON ФУНКЦИОНАЛЬНОСТЬ ")

    print("\n1. ФУНКЦИИ КАК ОБЪЕКТЫ:")
    print(f"  apply_function(square, 5) = {apply_function(square, 5)}")
    double = create_multiplier(2)
    triple = create_multiplier(3)
    print(f"  double(10) = {double(10)}")
    print(f"  triple(10) = {triple(10)}")

    print("\n2. LAMBDA-ФУНКЦИИ:")
    print(f"  squares = {squares}")
    print(f"  even_numbers = {even_numbers}")

    print("\n3. MAP/FILTER/REDUCE:")
    print(f"  student_names = {student_names}")
    print(f"  top_students = {[s['name'] for s in top_students]}")
    print(f"  product 1-10 = {product}")

    print("\n4. LIST COMPREHENSIONS:")
    print(f"  squares_lc = {squares_lc}")
    print(f"  even_squares = {even_squares}")

    print("\n5. ДЕКОРАТОРЫ:")
    slow_function()
    expensive_operation(5)

    print("\n6. КЭШИРОВАНИЕ:")
    print(f"  fibonacci(10) = {fibonacci(10)}")
    print(f"  fibonacci(10) = {fibonacci(10)}")  # Из кэша

    print("\n7. ПРАКТИЧЕСКИЕ ЗАДАНИЯ:")
    analysis = analyze_students(students)
    print(f"  Анализ студентов: {analysis}")
    
    print("  Логгер:")
    print(multiply(4, 5))
    
    print("  Простые числа:")
    primes = list(prime_generator(20))
    print(f"  {primes}")


if __name__ == "__main__":
    main()
