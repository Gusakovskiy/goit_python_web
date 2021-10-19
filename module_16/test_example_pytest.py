import pytest


@pytest.fixture(scope='function', autouse=True)
def my_function_scope_fixture():
    # setUP
    print('Will be used in each test')
    yield {'some_value': 'a'}
    # tearDown


@pytest.fixture(scope='session', autouse=True)
def my_session_scope_fixture():
    # setUP
    print('Will be executed one per session')
    yield {'some_value': 'a'}
    # tearDown
    print('Will be executed one per session')


def my_upper(value: str) -> str:
    return value.upper() if 'baz' not in value else value.capitalize()


@pytest.mark.parametrize(
    'value,expected',
    [
        pytest.param(
            'foo', 'FOO',
            id='regular foo',
        ),
        pytest.param(
            'baz', 'Baz',
            id='regular baz',
        ),
        # test without id
        ('foo baz', 'Foo baz')
    ]
)
def test_upper_foo(value, expected):
    assert my_upper(value) == expected
