import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from .env import *

TEMPLATE = """
Context: You anonymize texts in a way that can be reverted and return nothing but a json dictionary that can be parsed automatically.
Task instructions: Analyze the text provided after 'Text to anonymize' carefully for all names of persons and places.
For each name that you find evaluate whether it is a new name or just a repetition or variation of a name you have already found before.
Names of persons are labeled as #person_1#, #person_2#, etc. Names of places are labeled as #place_1#, #place_2#, etc.
Only return a json dictionary without any comments or markdown formatting around it. Do not return keys without values.
Example input: 'Tony Stark and Peter Parker walk through New York where Peter wants to show Tony the Broadway.'.
Example output: {{"#person_1#": ["Tony Stark", "Tony"], "#person_2#": ["Peter Parker", "Peter"], "#place_1#": ["New York"], "#place_2#": ["Broadway"]}}
Text to anonymize: {text}
"""

def llm_find_entities(text, temperature=0, template=TEMPLATE, raw=False):
    """
    :param text:
    :param model:
    :param temperature:
    :param template:
    :param raw:
    :return:
    """
    prompt = ChatPromptTemplate.from_template(template)


    model = OllamaLLM(model=OLLAMA_MODEL, temperature=temperature, base_url=OLLAMA_BASE_URL, client_kwargs={"verify": os.getenv("HTTPX_CLIENT_VERIFY", True)})
    chain = prompt | model
    result = chain.invoke({"text": text})
    if raw:
        return result
        
    ret = {k: v for k, v in json.loads(result).items()}
    return {k: set(v) for k, v in ret.items() if v}
