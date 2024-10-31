import json

def replace_values(text, replacements) -> str:
    # Iterate through the keys in the replacements dictionary
    for key, values in replacements.items():
        # Replace occurrences of each value with the corresponding key
        for value in values:
            text = text.replace(value, key)
    return text