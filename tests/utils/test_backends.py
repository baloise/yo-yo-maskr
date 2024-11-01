import pytest
from src.utils.ano_spacy import Anon_Spacy
from src.utils.ano_regex import find_entities as reg_find_entities
from src.utils.ano_llm import find_entities as llm_find_entities

if __name__ == "__main__":
    print(Anon_Spacy().find_entities("Hallo Roberto, how are you?"))

testData = [
    ("Hello there", {'text': 'Hello there','replace_dict': {}}),
    ("Roberto, how are you?", {'text': '#PERSON_1#, how are you?','replace_dict': {'#PERSON_1#': {'matches': {'Roberto'}, 'replacement': 'Roberto'}}}),
]

@pytest.mark.parametrize("input,expected", testData, ids=[f"#{i+1}" for i in range(len(testData))])
@pytest.mark.parametrize("testee", [
    (llm_find_entities),
    (reg_find_entities),
    (Anon_Spacy().find_entities),
],
 ids=["LLM"
         , "REG"
         , "NER"
         ]
    )
def test_backend(testee, input: str, expected: dict):
    print(f"Testing {testee.__name__} with input '{input}'")
    result = testee(input)
    print(f"Result: {result}")
    assert result == expected


