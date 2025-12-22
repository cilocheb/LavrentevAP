def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    if b == 0:
        raise ValueError("Division by zero")
    return a / b


def main():
    print("Простой калькулятор. Пример: 3 + 4")
    expr = input("Введите выражение: ")
    a, op, b = expr.split()
    a = float(a)
    b = float(b)
    ops = {"+": add, "-": sub, "*": mul, "/": div}
    print(ops[op](a, b))


if __name__ == "__main__":
    main()
