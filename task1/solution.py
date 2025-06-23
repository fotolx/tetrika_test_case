import unittest

def strict(func):
    arg_types = tuple(func.__annotations__.values())
    def wrapper(*args, **kwargs):
        if not all(type(a) is t for a, t in zip(args, arg_types)):
            raise TypeError
        return func(*args, **kwargs)
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b

class TestStrictDecorator(unittest.TestCase):
    def test_correct_int_types(self):
        @strict
        def add(a: int, b: int) -> int:
            return a + b
        self.assertEqual(add(1, 2), 3)
    def test_correct_bool_types(self):
        @strict
        def logical_and(a: bool, b: bool) -> bool:
            return a and b
        self.assertEqual(logical_and(True, False), False)
    def test_correct_float_types(self):
        @strict
        def float_sub(a: float, b: float) -> float:
            return a - b
        self.assertEqual(float_sub(2.5, 1.75), .75)
    def test_correct_str_types(self):
        @strict
        def concat(a: str, b: str) -> str:
            return a + b
        self.assertEqual(concat('Hello, ', 'world!'), 'Hello, world!')
    def test_incorrect_types_str_not_int(self):
        @strict
        def add(a: int, b: int) -> int:
            return a + b
        with self.assertRaises(TypeError):
            add(1, '2')
    def test_incorrect_types_bool_not_int(self):
        @strict
        def add(a: int, b: int) -> int:
            return a + b
        with self.assertRaises(TypeError):
            add(1, True)
    def test_incorrect_types_int_not_bool(self):
        @strict
        def logical_or(a: bool, b: bool) -> bool:
            return a or b
        with self.assertRaises(TypeError):
            logical_or(1, True)
    def test_incorrect_types_int_not_float(self):
        @strict
        def divide(a: float, b: float) -> float:
            return a / b
        with self.assertRaises(TypeError):
            divide(3., 2)
    def test_three_arguments(self):
        @strict
        def multiply(a: int, b: int, c: int) -> int:
            return a * b * c
        self.assertEqual(multiply(1, 2, 3), 6)
    def test_all_types(self):
        @strict
        def Making_a_New_Science(is_correct: bool, name: str, year: int, amount: float) -> str:
            return f'{is_correct}, {name}\'s {year} model required just {amount} perturbation to trigger the butterfly effect.'
        self.assertEqual(Making_a_New_Science(True, name='Lorenz', year=1963, amount=0.001), 'True, Lorenz\'s 1963 model required just 0.001 perturbation to trigger the butterfly effect.')

if __name__ == '__main__':
    # Запуск тестов
    unittest.main(argv=[''], exit=False)

    print(sum_two(1, 2))  # >>> 3
    # print(sum_two(1, 2.4))  # >>> TypeError