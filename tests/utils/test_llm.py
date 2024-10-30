import pytest
from src.utils.llm import llm_find_entities

def test_llm_find_entities_basic():
    text = "Tony Stark and Peter Parker walk through New York where Peter wants to show Tony the Broadway."
    expected_output = {'#person_1#': {'Tony Stark', 'Tony'}, '#person_2#': {'Peter Parker', 'Peter'}, '#place_1#': {'New York'}, '#place_2#': {'Broadway'}}
    result = llm_find_entities(text)
    assert result == expected_output
    assert result == expected_output

def test_llm_find_entities_no_entities():
    text = "This is a text without any names of persons or places."
    expected_output = {}
    result = llm_find_entities(text)
    assert result == expected_output

def test_llm_find_entities_repeated_names():
    text = "Alice and Bob went to Wonderland. Alice met Bob at the Wonderland park."
    expected_output = {
        "#person_1#": ["Alice"],
        "#person_2#": ["Bob"],
        "#place_1#": ["Wonderland"],
        '#place_2#': ['Wonderland park']
    }
    result = llm_find_entities(text)

def test_llm_find_entities_raw_output():
    text = "Tony Stark and Peter Parker walk through New York where Peter wants to show Tony the Broadway."
    result = llm_find_entities(text, raw=True)
    print("result")
    print(result)
    assert isinstance(result, str)
    assert "Tony Stark" in result
    assert "Peter Parker" in result
    assert "New York" in result
    assert "Broadway" in result