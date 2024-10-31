import pytest

def add(x, y):
    return x + y

@pytest.mark.parametrize("x,y,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, -2, -3),
    (10, 5, 15),
])

def test_add(x, y, expected):
    assert add(x, y) == expected

def assert_backend(testee: any, input: str, expected: dict):
    assert testee.find_entities(input) == expected

def find_entities():

    testee = Anon_Spacy()
    assert_backend(testee, "input", )