def revert_replacements(masked_text, entity_dict):
    for key, value in entity_dict.items():
        masked_text = masked_text.replace(key, value['replacement'])
    return masked_text