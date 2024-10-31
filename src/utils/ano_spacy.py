import spacy
import spacy.cli
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
#from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer.nlp_engine import SpacyNlpEngine, NlpEngineProvider
from presidio_analyzer.predefined_recognizers import SpacyRecognizer
from presidio_analyzer import PatternRecognizer

class Anon_Spacy:
    def __init__(self):
        languages = ['en','de','fr','it']
        size = "lg"
        gernres = {lang: "web" if lang == 'en' else "news" for lang in languages}
        self.models = {lang: f"{lang}_core_{gernres[lang]}_{size}" for lang in languages}
        self.models_loaded = []

    def analyze_text(self, text, language='de',entities=['PERSON']):
        if not language in self.models:
            print(f"WARN: language '{language}' not supported. Supported languages are {self.models.keys()}.")
        return self.get_analyzer(language,entities).analyze(text=text, language=language, entities=["PERSON"])
    
    def get_analyzer(self,language='de',entities=['PERSON']):
        self.ensure_model_loaded(self.models[language])
        nlp_engine = SpacyNlpEngine(models=[{"lang_code": language, "model_name": self.models[language]}])
        analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=[language])
        analyzer.registry.add_recognizer(SpacyRecognizer(supported_language=language, supported_entities=entities))
        return analyzer

    def ensure_model_loaded(self,model_name):
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

# Add custom recognizers if needed
# Example: Adding a custom recognizer for French phone numbers
# fr_phone_recognizer = PatternRecognizer(supported_entity="FR_PHONE_NUMBER", 
#                                         patterns=[{"name": "FR_PHONE", 
#                                                    "regex": r"(\+33|0)[1-9]\d{8}", 
#                                                    "score": 0.9}])
# analyzer.registry.add_recognizer(fr_phone_recognizer)


# Initialize the anonymizer engine
#anonymizer = AnonymizerEngine()


# def anonymize_text(text, language):
#     return anonymizer.anonymize(text=text, analyzer_results=analyze_text(text,language))