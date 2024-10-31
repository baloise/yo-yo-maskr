import json

def revert_replacements(text, replacements) -> str:
    reversed_replacements = {}
    
    for key, values in replacements.items():
        for value in values:
            if value not in reversed_replacements:
                reversed_replacements[value] = []
            reversed_replacements[value].append(key)
    
    for value, keys in reversed_replacements.items():
        for key in keys:
            text = text.replace(key, value['matches'])
    
    return text
