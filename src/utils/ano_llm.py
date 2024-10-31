import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from .env import *



TEMPLATE = """
Context: Your task is to find persons, locations, organizations, email addresses and telephone numbers in a text
and tag them in a way that they can be anonymized in a reversible way.

Task instructions: 

General:
Find all names of people, organizations and locations and return nothing but a json with all those entities.
Work through the following steps and stick as close as only possible to the structure provided in the example output.

Step 1: You analyze the text provided after "Text to anonymize" carefully for names of people, organizations, locations, email addresses and telephone numbers.
Create a list of all those entities that you have found.
Do not include the result of this step in your output.

Step 2: You go through all those entities that you found and evaluate for each entity whether it is a new entity
or just a repetition or variation of an already found entity. Group all variations of individual entities together. 
If you are not sure whether an entity is a new entity or a variation of an already found entity, play it safe and assume it to be a new entity.
Do not include the result of this step in your output.

Step 3: you build a json style dictionary directly be parsed by Python into an object structure
with labels as keys and lists of variations of names as values. Stick exactly to this structure and don't add anything around that json.
Labels of persons are enumerated #NAME_1#, #NAME_2#, etc. always beginning with index 1.
Labels of organisations as #ORG_1#, #ORG_2#, etc. always beginning index with 1.
Labels of email addresses as #EMAIL_1#, #EMAIL_2#, etc. always beginning with index 1.
Labels of phone numbers as #PHONE_1#, #PHONE_2#, etc. always beginning with index 1.
Only use labels for those entities that you found. It is possible that you don't need all types of labels.
This json style dictionary is the only output that you return.

Example:
Input: "Tony Stark and Peter Parker walk through New York where Peter wants to show Tony the Broadway and the Apple Store. Tony's email is tony@stark.com".
Output: {{"#NAME_1#":["Tony Stark", "Tony"], "#NAME_2#": ["Peter Parker", "Peter"], "#LOC_2#": ["New York"], "#LOC_2#": ["Broadway"], "ORG_1": ["Apple"], "#EMAIL_1#": ["tony@stark.com"]}}

Text to anonymize: {text}
"""

def find_entities(text, model_name=OLLAMA_MODEL, temperature=0, template=TEMPLATE,
                   base_url=OLLAMA_BASE_URL, raw=False):
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
    result = {k: {'matches': (m:=sorted(v, key=len, reverse=True)), 'replacement': m[0]} for k, v in json.loads(result.strip()).items()}
    return result
