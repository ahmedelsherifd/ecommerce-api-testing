import pytest

from main import wrong_attempts


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    yield
    wrong_attempts.clear()
