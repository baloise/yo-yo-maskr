import json

def replace_values(text, replacements) -> str:
    # Iterate through the keys in the replacements dictionary
    for key, values in replacements.items():
        # Replace occurrences of each value with the corresponding key
        for value in values:
            text = text.replace(value, key)
    return text

def revert_replacements(text, replacements) -> str:
    # Create a new dictionary to hold the reversed replacements
    reversed_replacements = {}
    
    # Iterate through the keys and values in the replacements dictionary
    for key, values in replacements.items():
        for value in values:
            # Add the key to the reversed dictionary with the corresponding value
            if value not in reversed_replacements:
                reversed_replacements[value] = []
            reversed_replacements[value].append(key)
    
    # Iterate through the reversed replacements and replace keys with their values
    for value, keys in reversed_replacements.items():
        for key in keys:
            text = text.replace(key, value)
    
    return text