import unittest


def my_upper(value: str) -> str:
    return value.upper() if 'baz' not in value else value.capitalize()


class TestMyUpper(unittest.TestCase):

    def setUp(self):
        super().setUp()
        print('Will be executed before each test\n')

    def tearDown(self) -> None:
        super().tearDown()
        print('Will be executed after each test\n')

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        print('*' * 42)
        print('Will be executed before start of testsuit\n')

    @classmethod
    def tearDownClass(cls) -> None:
        super().setUpClass()
        print('*' * 42)
        print('Will be executed after start of testsuit\n')

    def test_upper_foo(self):
        self.assertEqual(my_upper('foo'), 'FOO')

    def test_upper_baz(self):
        self.assertEqual(my_upper('baz'), 'Baz')

    def test_upper_baz_in(self):
        self.assertEqual(my_upper('foo baz'), 'Foo baz')


if __name__ == '__main__':
    # python -m unittest test_example_unittest.py
    unittest.main()