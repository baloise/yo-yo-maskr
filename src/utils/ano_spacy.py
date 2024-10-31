import spacy
import spacy.cli
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import SpacyNlpEngine, NlpEngineProvider
from presidio_analyzer.predefined_recognizers import SpacyRecognizer
from presidio_analyzer import PatternRecognizer
import sys

class Anon_Spacy:
    def __init__(self):
        languages = ['en','de','fr','it']
        size = "lg"
        gernres = {lang: "web" if lang == 'en' else "news" for lang in languages}
        self.models = {lang: f"{lang}_core_{gernres[lang]}_{size}" for lang in languages}
        self.models_loaded = []

    def _create_dict(self, text:str, analysis:list)->dict:
        replace_dict:dict = {}
        text_with_placeholders:str = text
        for i, entity in enumerate(analysis):
            if not entity['entity'] in replace_dict.keys():
                placeholder = f"#NAME_{i+1}#"
                replace_dict[entity['entity']] = placeholder
                text_with_placeholders = text_with_placeholders.replace(str(entity['entity']), placeholder)
        return {'text': text_with_placeholders, 'replace_dict': replace_dict}

    def anonymize_names(self, text, language='de'):
        return self._create_dict(text, self.analyze_text(text, language))

    def analyze_text(self, text, language='de',entities=['PERSON']):
        if not language in self.models:
            print(f"WARN: language '{language}' not supported. Supported languages are {self.models.keys()}.")
        analysis = self._get_analyzer(language, entities).analyze(text=text+'.', language=language, entities=["PERSON"])
        results = []
        for result in analysis:
            results.append({
            "start": result.start,
            "end": result.end,
            "entity_type": result.entity_type,
            "score": result.score,
            "entity": text[result.start:result.end]
            })
        return results
    
    def _get_analyzer(self,language='de',entities=['PERSON']):
        self._ensure_model_loaded(self.models[language])
        nlp_engine = SpacyNlpEngine(models=[{"lang_code": language, "model_name": self.models[language]}])
        analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=[language])
        analyzer.registry.add_recognizer(SpacyRecognizer(supported_language=language, supported_entities=entities))
        return analyzer

    def _ensure_model_loaded(self,model_name):
        if model_name in self.models_loaded:
            print(f"Model '{model_name}' already loaded.")
            return
        print(f"Loading model '{model_name}'.")
        try:
            # Try to load the model
            return spacy.load(model_name)
        except OSError:
            # If the model is not found, download it
            print(f"Model '{model_name}' not found. Downloading...")
            spacy.cli.download(model_name)
            print(f"Model '{model_name}' downloaded successfully.")
            return spacy.load(model_name)
        finally:
            self.models_loaded.append(model_name)
            print(f"Model '{model_name}' loaded.")

if __name__ == "__main__":
    if "loadModels" in sys.argv:
        anon = Anon_Spacy()
        for model in anon.models.values():
            anon._ensure_model_loaded(model)
        print("All models loaded.")