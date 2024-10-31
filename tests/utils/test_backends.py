import pytest
from src.utils.ano_spacy import Anon_Spacy
from src.utils.ano_regex import find_entities as reg_find_entities
from src.utils.ano_llm import find_entities as llm_find_entities

testees = [
            reg_find_entities, 
            llm_find_entities,
        #    Anon_Spacy().find_entities
           ]


if __name__ == "__main__":
    print(repr(llm_find_entities))
    print(llm_find_entities("Hello there"))


@pytest.mark.parametrize("input,expected", [
    ("Hello there", {'text': 'Hello there','replace_dict': {}}),
])
def test_backend( input: str, expected: dict):
    for index, testee in enumerate(testees):
        print(f"Iteration {index}")
        print(f"Testing {testee.__name__} with input '{input}'")
        result = testee(input)
        print(f"Result: {result}")
        assert result == expected
