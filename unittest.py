import pytest
from main import eightbyeightQueen

@pytest.fixture
def test_utility_fn():
    x = eightbyeightQueen()
    gen = [4, 7, 3, 0, 6, 1, 5, 2]
    y = x.utilityFunction(gen)
    assert y == 0

