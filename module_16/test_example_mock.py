import pytest
import logging
from unittest.mock import MagicMock, patch

logger = logging.getLogger(__name__)


def my_add(a, b):
    if a != 42:
        logger.error('Got not 42 as first value %s', a)
        raise ValueError('First argument should be 42')
    return a + b


@pytest.fixture(scope='function')
def mock_logger_fixture():
    logger.error = MagicMock()
    yield logger.error


def test_my_add(mock_logger_fixture):
    a = 43
    b = 10
    mocked_error = mock_logger_fixture
    with pytest.raises(ValueError):
        my_add(a, b)

    mocked_error.assert_called_once_with(
        'Got not 42 as first value %s', a
    )
    mocked_error.assert_called_once()
    # mocked_error.assert_not_called()


def test_my_add_patch():
    # with patch('module_16.test_example_mock.logger.error', return_value=None)  as mocked_error:
    with patch.object(logger, 'error', return_value=None) as mocked_error:
        my_add(42, 16)
        mocked_error.assert_not_called()