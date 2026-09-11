import pytest

from app import total_cost


@pytest.mark.parametrize("items,discount,expected", [
    ([10, 20], 0, 30),
    ([10, 20], 10, 27),
    ([], 0, 0),
    ([10], 100, 0),
    ([1.99, 2.99], 5, 4.73),
])
def test_total(items, discount, expected):
    assert total_cost(items, discount) == expected


@pytest.mark.parametrize("discount", [-1, 101])
def test_invalid_discount(discount):
    with pytest.raises(ValueError):
        total_cost([10], discount)


def test_negative_price():
    with pytest.raises(ValueError):
        total_cost([-1])
