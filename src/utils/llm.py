import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from .env import *

TEMPLATE = """
Context: You anonymize texts in a way that can be reverted and return nothing but a json dictionary that can be parsed automatically.
Task instructions: Analyze the text provided after 'Text to anonymize' carefully for all names of persons and places.
For each name that you find evaluate whether it is a new name or just a repetition or variation of a name you have already found before.
Names of persons are labeled as #NAME_1#, #NAME_2#, etc. Names of places are labeled as #PLACE_1#, #PLACE_2#, etc. E-mail addresses are labeled as #EMAIL_1#, #EMAIL_2#, etc.
Only return a json dictionary without any comments or markdown formatting around it. Do not return keys without values.
Example input: 'Tony Stark and Peter Parker walk through New York where Peter wants to show Tony the Broadway. My E-mai is tony.stark@stark.com.'.
Example output: {{"#NAME_1#": ["Tony Stark", "Tony"], "#NAME_2#": ["Peter Parker", "Peter"], "#PLACE_1#": ["New York"], "#PLACE_2#": ["Broadway"], "#EMAIL_1#": ["tony.stark@stark.com"]}}
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


if __name__ == "__main__":

    llm_entities = {
        "#NAME_1#": [
            "Hallo",
            "Velo"
        ],
        "#NAME_2#": [
            "Roberto"
        ],
        "#PLACE_1#": [
            "Basel"
        ],
        "#EMAIL_1#": [
            "roberto@roberto.ch"
        ],
        "#EMAIL_2#": [
            "matthias@matthias.ch"
        ]
    }

    want ={
        "text": "Hallo Velo und #PERSON_1# in Basel. Nice email #EMAIL_2# and #EMAIL_1# and \n\n#EMAIL_2#",
        "replace_dict": {
            "#EMAIL_2#": {
            "matches": [
                "roberto@roberto.ch"
            ],
            "replacement": "roberto@roberto.ch"
            },
            "#EMAIL_1#": {
            "matches": [
                "matthias@matthias.ch"
            ],
            "replacement": "matthias@matthias.ch"
            },
            "#PERSON_1#": {
            "matches": [
                "Roberto"
            ],
            "replacement": "Roberto"
            }
        }
    }