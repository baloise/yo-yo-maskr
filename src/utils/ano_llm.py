import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from src.utils.env import *


TEMPLATE = """
Context: Your task is to find  entities in a text and tag them in a way that they can be anonymized in a reversible way.
The entity types are persons, locations, organizations, email addresses and telephone numbers.
Be very careful to not miss an entity. It is better to wrongly flag some expression as entity than to miss an entity.
You want to group persons, locations and organizations but you must be absolutely certain that entities you group refer to the same person, location or organization.
If you are in doubt whether an entity is a new entity or a variation of an already found entity, be on the safe side and assume it to be a new entity.

Task instructions: 

General:
Find all names of people, organizations, locations, email addresses and return nothing but a json that can be directly parsed by Python with all those entities.
Work through the following steps and stick as close as only possible to the structure provided in the example output.

Step 1: Analyze the text provided after "Text to anonymize" carefully for names of people, organizations, locations, email addresses and telephone numbers.
Do not include the result of this step in your output.

Step 2: For names of people, organizations, and locations go through all those entities that you found and evaluate for each entity whether it is a new entity
or just a variation of an already found entity. Use the following guidelines:
a) Lists of names, locations or organizations such as Peter, Paul and Mary are almost certainly different entities.
b) Treat all Email addresses and phone numbers that you find as different entities.
Do not include the result of this step in your output.

Step 3: You build a json style dictionary directly be parsed by Python into an object structure
with labels as keys and lists of variations of entities as values. Stick exactly to this structure and don't add anything around that json.
a) Labels of persons are enumerated #PERSON_1#, #PERSON_2#, etc. always beginning with index 1.
b) Labels of organisations as #ORG_1#, #ORG_2#, etc. always beginning index with 1.
c) Labels of email addresses as #EMAIL_1#, #EMAIL_2#, etc. always beginning with index 1.
d) Labels of phone numbers as #PHONE_1#, #PHONE_2#, etc. always beginning with index 1.
Only use labels for those entities that you found. It is possible that there are no entities for a kind of labels.
This json style dictionary is the only output that you return.

Example:
Input: "Tony Stark and Peter Parker walk through New York where Peter wants to show Tony the Broadway and the Apple Store.
Tony's private email is tony@stark.com, his busienss email is ceo@stark.com, his private number is +41-76-1234567 and his business number is +41 58 1234567".
Output: {{"#PERSON_1#":["Tony Stark", "Tony"], "#PERSON_2#": ["Peter Parker", "Peter"], "#LOC_1#": ["New York"], "#LOC_2#": ["Broadway"],
"ORG_1": ["Apple"], "#EMAIL_1#": ["tony@stark.com"], "#EMAIL_2#": ["ceo@stark.com"], "#PHONE_1#": ["+41-76-1234567"], “PHONE_2#: ["+41 58 1234567"]}}

Text to anonymize: {text}
"""

def find_entities(text, model_name=OLLAMA_MODEL, temperature=0, template=TEMPLATE, base_url=OLLAMA_BASE_URL, raw=False):
    """
    :param text:
    :param model:
    :param temperature:
    :param template:
    :param base_url:
    :param raw:
    :return:
    """
    
    
    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model=model_name, temperature=temperature, base_url=base_url, client_kwargs={"verify": os.getenv("HTTPX_CLIENT_VERIFY", True)})
    chain = prompt | model

    result = chain.invoke({"text": text})
    if raw:
        return result
    result = {k: {'matches': (m:=sorted(list(set(v)), key=len, reverse=True)), 'replacement': m[0]} for k, v in json.loads(result).items() if len(v) > 0}
    for k, v in result.items():
        text = text.replace(v.get('replacement'), k)
    return {'text': text, 'replace_dict': result}
