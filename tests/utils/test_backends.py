import pytest
from src.utils.ano_spacy import Anon_Spacy
from src.utils.ano_regex import find_entities as reg_find_entities
from src.utils.ano_llm import find_entities as llm_find_entities

if __name__ == "__main__":
    print(Anon_Spacy().find_entities("Hello there"))


@pytest.mark.parametrize("input,expected", [
    ("Hello there", {'text': 'Hello there','replace_dict': {}}),
    #("Hallo Roberto, how are you?", {'text': 'Hallo #PERSON_1#, how are you?','replace_dict': {'#PERSON_1#': {'matches': {'Roberto'}, 'replacement': 'Roberto'}}}),
])
@pytest.mark.parametrize("testee", [
    (reg_find_entities),
    (llm_find_entities),
    (Anon_Spacy().find_entities),
])
@pytest.mark.filterwarnings("ignore:PluggyTeardownRaisedWarning")
def test_backend(testee, input: str, expected: dict):
    print(f"Testing {testee.__name__} with input '{input}'")
    result = testee(input)
    print(f"Result: {result}")
    assert result == expected
