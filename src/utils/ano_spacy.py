import spacy
import spacy.cli
import sys

class Anon_Spacy:
    def __init__(self):
        languages = ['en','de','fr','it']
        size = "lg"
        gernres = {lang: "web" if lang == 'en' else "news" for lang in languages}
        self.models = {lang: f"{lang}_core_{gernres[lang]}_{size}" for lang in languages}
        self.models_loaded = {}

    def _create_dict(self, text:str, analysis:list)->dict:
        replace_dict:dict = {}
        text_with_placeholders:str = text
        for i, entity in enumerate(analysis):
            if not entity['entity'] in replace_dict.keys():
                placeholder = f"#NAME_{i+1}#"
                replace_dict[entity['entity']] = placeholder
                text_with_placeholders = text_with_placeholders.replace(str(entity['entity']), placeholder)
        return {'text': text_with_placeholders, 'replace_dict': replace_dict}

    def find_entities(self, text, language='de'):
        return self._create_dict(text, self.analyze_text(text, language))

    def analyze_text(self, text, language='de',entities=['PERSON']):
        if not language in self.models:
            print(f"WARN: language '{language}' not supported. Supported languages are {self.models.keys()}.")
        analysis = self._get_analyzer(language)(text)
        results = []
        for result in analysis.ents:
            if(result.label_ in entities):
                results.append({
                "start": result.start_char,
                "end": result.end_char,
                "entity_type": result.label_,
                "entity": result.ents[0] #text[result.start_char:result.end_char]
                })
        return results
    
    def _get_analyzer(self,language):
        model_name = self.models[language]
        if model_name in self.models_loaded.keys():
            print(f"Model '{model_name}' already loaded.")
            return self.models_loaded[model_name]
        print(f"Loading model '{model_name}'.")
        try:
            # Try to load the model
            self.models_loaded[model_name] = spacy.load(model_name)
            print(f"Model '{model_name}' loaded.")
            return self.models_loaded[model_name]
        except OSError:
            # If the model is not found, download it
            print(f"Model '{model_name}' not found. Downloading...")
            spacy.cli.download(model_name)
            print(f"Model '{model_name}' downloaded successfully.")
            return self._get_analyzer(model_name)

if __name__ == "__main__":
    if "loadModels" in sys.argv:
        anon = Anon_Spacy()
        for model in anon.models.values():
            anon._get_analyzer(model)
        print("All models loaded.")