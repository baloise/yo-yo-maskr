import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import regex as re
from .env import *

TEMPLATE1 = """
Context: Your task is to find entities in a text and tag them in a way that they can be anonymized in a reversible way.
The entity types are persons, locations, organizations, email addresses, telephone numbers and social security numbers.
Be very careful to not miss an entity. It is better to wrongly flag some expression as an entity than to miss an entity.
If you are absolutely certain that two or more found entities are just different variations of the same entity, you may group them.
If you are in doubt or not sure, be on the safe side and treat them asdifferent entities that can not be grouped together.
Expect the majority of entities you find to not be variations of the same entity.

Task instructions: 

General:
Find all names of people, organizations, locations, email addresses and return nothing but a json that can be directly parsed by Python with all those entities.
Work through the following steps and stick as close as only possible to the structure provided in the example output.

Step 1: Analyze the text provided after "Text to anonymize" carefully for names of people, organizations, locations, email addresses and telephone numbers.
Do not include the result of this step in your output.

Step 2: For names of people, organizations, and locations go through all those entities that you found and evaluate for each entity whether it is a new entity
or just a variation of an already found entity. Use the following guidelines:
a) If two expressions are not exactly identical, it is more likely that they are different entities.
a) Lists of names, locations or organizations such as Peter, Paul and Mary are almost certainly different entities.
b) Treat all Email addresses and phone numbers that you find as different entities.
c) Social security numbers have a standardized format depending on the country. Use any country specific format you are aware of
such as 756.XXXX.XXXX.XX (Switzerland), YYMMDD-XXX-XX (Belgium), 12-345678A 123 (Germany) or (YYYYMMDDXXXX) Luxembourg.
Do not include the result of this step in your output.

Step 3: You build a json style dictionary directly be parsed by Python into an object structure
with labels as keys and for each label a list of variations of an entity as values.
Stick exactly to this structure and don't add anything around that json.
a) Labels of persons are enumerated #NAME_1#, #NAME_2#, etc. always beginning with index 1.
b) Labels of organisations as #ORG_1#, #ORG_2#, etc. always beginning index with 1.
c) Labels of email addresses as #EMAIL_1#, #EMAIL_2#, etc. always beginning with index 1.
d) Labels of phone numbers as #PHONE_1#, #PHONE_2#, etc. always beginning with index 1.
e) Labels of social security nubers as #SOCSEC_1#, #SOCSEC_2#, etc. always beginning with index 1.
Only use labels for those entities that you found. It is possible that there are no entities for a kind of labels.
Do not include the result of this step in your output yet.

Step 4: Double check your grouping.
Are all entities you grouped together really just variations of the same entity or should they have been different entities?
If necessary, split such groups of entities. Make sure that each sort of labels keeps a continuous numbering beginning with 1.
This json style dictionary is the only output that you return.

Example input:
"Tony Stark and Peter Parker walk through New York where Peter wants to show Tony the Broadway and the Apple Store.
Tony's private email is tony@stark.com, his busienss email is ceo@stark.com, his private number is +41-76-1234567 and his business number is +41 58 1234567.
He also has an AHV number, which is 756.1234.5678.90".

Example output:
{{"#NAME_1#": ["Tony Stark", "Tony"],"#NAME_2#": ["Peter Parker", "Peter"],"#LOC_1#": ["New York"],"#LOC_2#": ["Broadway"],"#ORG_1#": ["Apple"],"#EMAIL_1#": ["tony@stark.com"],"#EMAIL_2#": ["ceo@stark.com"],"#PHONE_1#": ["+41-76-1234567"],"#PHONE_2#": ["+41 58 1234567"],"#SOCSEC_1#": ["756.1234.5678.90"]}}

Text to anonymize: {text}
"""



TEMPLATE2 = """
**Objective**:
Identify and tag entities in the provided text for reversible anonymization, focusing on Switzerland, Germany, Belgium, and Luxembourg. The relevant categories include **persons, locations, organizations, email addresses, telephone numbers, social security numbers, dates, addresses, financial information**, and **credit card information**. Accurate tagging is critical; it is preferable to flag non-entities than to miss actual entities. If certain entities are variations of the same, you may group them; however, when in doubt, treat them as separate. Expect most entities to be unique.

**ask Instructions**:

1. **Identify Entities**:
   - Analyze the provided text for **names of people, organizations, locations, email addresses, telephone numbers, social security numbers, dates, addresses, financial information,** and **credit card information**. Ensure to account for the three official languages of Switzerland (German, Italian, and French) and the languages spoken in Germany, Belgium, and Luxembourg.
   - Do **not** include the result of this step in your output.

2. **Evaluate Entity Grouping**:
   - Determine if each entity is unique or a variation:
     - Treat non-identical expressions as distinct entities unless they are clearly variations.
     - Lists (e.g., "Peter, Paul, and Mary") typically contain unique entities.
     - Treat each **email address, phone number, social security number, date, address, financial information,** and **credit card information** as unique.

3. **Social Security Number and Telephone Number Formats**:
   - Recognize social security numbers in known country formats:
     - **Switzerland**: "756.XXXX.XXXX.XX"
     - **Germany**: "12-345678A 123"
     - **Belgium**: "YYMMDD-XXX-XX"
     - **Luxembourg**: "YYYYMMDDXXXX"
   - Recognize telephone numbers in the following formats:
     - **Switzerland**: "+41 12 345 67 89" or "+41-12-345-67-89"
     - **Germany**: "+49 30 1234567" or "030 1234567"
     - **Belgium**: "+32 2 123 45 67" or "02 123 45 67"
     - **Luxembourg**: "+352 123 456" or "123 456"

4. **Create JSON Output**:
   - Format the JSON dictionary to be directly parsable by Python without any unwanted formatting or escape characters.
   - **Labels** should strictly follow this format, with continuous numbering starting at 1 for each category:
     - **Persons**: "#NAME_1#", "#NAME_2#", etc.
     - **Organizations**: "#ORG_1#", "#ORG_2#", etc.
     - **Locations**: "#LOC_1#", "#LOC_2#", etc.
     - **Emails**: "#EMAIL_1#", "#EMAIL_2#", etc.
     - **Phone numbers**: Use "#PHONE_1#", "#PHONE_2#", etc. (follow country formats listed above).
     - **Social security numbers**: Use only "#SOCSEC_1#", "#SOCSEC_2#", etc. (follow country formats listed above).
     - **Dates**: "#DATE_1#", "#DATE_2#", etc.
     - **Addresses**: "#ADDRESS_1#", "#ADDRESS_2#", etc.
     - **Financial information**: "#FINANCE_1#", "#FINANCE_2#", etc.
     - **Credit card information**: "#CREDITCARD_1#", "#CREDITCARD_2#", etc.
   - **Output Schema**:
     Please return a JSON object that follows this schema:
     {{"#NAME_x#": ["list of names"],"#LOC_x#": ["list of locations"],"#ORG_x#": ["list of organizations"],"#EMAIL_x#": ["list of emails"],"#PHONE_x#": ["list of phone numbers"],"#SOCSEC_x#": ["list of social security numbers"],"#DATE_x#": ["list of dates"],"#ADDRESS_x#": ["list of addresses"],"#FINANCE_x#": ["list of financial information"],"#CREDITCARD_x#": ["list of credit card numbers"]}}
     Ensure that each key is followed by a non-empty list, and do not add any explanation or pretty print such as line breaks or ```json tags outside of this JSON format.
   - **Output Example**:
     {{"#NAME_1#": ["John Doe", "Herr Doe"],"#ORG_1#": ["ACME Corporation"],"#EMAIL_1#": ["john.doe@example.com"],"#PHONE_1#": ["+41 44 123 45 67"],"#SOCSEC_1#": ["756.1234.5678.90"],"#DATE_1#": ["2024-10-31"],"#ADDRESS_1#": ["Hauptstraße 123, Zürich"],"#FINANCE_1#": ["CHF 1'000"],"#CREDITCARD_1#": ["4111 1111 1111 1111"]}}

5. **Double-Check Grouping**:
   - Confirm that each grouping accurately reflects variations of the same entity. If necessary, split and renumber labels starting at 1 for each category.

6. **Double-Check JSON Structure**:
   - Confirm that the JSON object contains no additional text, tags, or formatting (such as ```json). Ensure that the output is a clean, valid JSON object free of escape sequences or code formatting, which can be directly parsed in programming languages like Python.
   - Remove any tags, formatting or explanations around the JSON object. The relevant objective is to make it parsable by Python, not readability or explanations.

**Output**:
   - Return only the JSON object.
   - Ensure the JSON is clean, valid, and directly parsable in Python.
   - No additional text, tags, explanations, or formatting should be included as these prevent the JSON from being directly parsable.

**Example input**:
"Tony Stark and Peter Parker walk through New York where Peter wants to show Tony the Broadway and the Apple Store.
Tony's private email is tony@stark.com, his busienss email is ceo@stark.com, his private number is +41-76-1234567 and his business number is +41 58 1234567.
He also has an AHV number, which is 756.1234.5678.90".

**Example output**:
{{"#NAME_1#": ["Tony Stark", "Tony"],"#NAME_2#": ["Peter Parker", "Peter"],"#LOC_1#": ["New York"],"#LOC_2#": ["Broadway"],"#ORG_1#": ["Apple"],"#EMAIL_1#": ["tony@stark.com"],"#EMAIL_2#": ["ceo@stark.com"],"#PHONE_1#": ["+41-76-1234567"],"#PHONE_2#": ["+41 58 1234567"],"#SOCSEC_1#": ["756.1234.5678.90"]}}


Text to anonymize: {text}   
"""


def find_entities(text, model=OLLAMA_MODEL, temperature=0.1, template=TEMPLATE2,
                  base_url=OLLAMA_BASE_URL, unprettify=True, raw=False):
    """
    :param text:
    :param model:
    :param temperature:
    :param template:
    :param base_url:
    :param unprettify:
    :param raw:
    :return:
    """
    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(base_url=base_url, model=model, temperature=temperature)
    chain = prompt | model
    result = chain.invoke({"text": text})
    if unprettify:
       result = re.search(r'{.*}', re.sub(r'\/\/.*|\/\*.*?\*\/', '',result, flags=re.DOTALL), re.DOTALL).group(0)
    if raw:
       return result
   
    result = {k: {'matches': (m:=sorted(list(set(v)), key=len, reverse=True)), 'replacement': m[0]}
              for k, v in json.loads(result.strip()).items() if len(v) > 0}
    for k, v in result.items():
        text = text.replace(v.get('replacement'), k)
    return {'text': text, 'replace_dict': result}
