import requests
import os

class TranslateAPIController:
    def __init__(self):
        self.API_KEY = os.getenv("API_KEY", "")
        self.url = f"https://translation.googleapis.com/language/translate/v2"
    
    def translate(self, source_text, source_lang, target_lang):
        source = "auto"
        if source_lang != "Identifica limba":
            source = source_lang

        self.params = {
            "q": source_text,
            "source": source,
            "target": target_lang,
            "key": self.API_KEY
        }
        try:
            response = requests.post(self.url, data=self.params)
            response.raise_for_status()
            translation = response.json()['data']['translations'][0]['translatedText']

            return translation
        
        except Exception as e:
            raise e

    def getSupportedLanguages(self):
        url = "https://translation.googleapis.com/language/translate/v2/languages"
        params = {
            "key": self.API_KEY,
            "target": "ro"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            languages = response.json()["data"]["languages"]
            return languages
        except Exception as e:
            raise e

    def detectLanguage(self, source_text):
        url = "https://translation.googleapis.com/language/translate/v2/detect"
        params = {
            "q": source_text,
            "key": self.API_KEY
        }
        try:
            response = requests.post(url, data=params)
            response.raise_for_status()
            language = response.json()["data"]["detections"][0][0]["language"]
            if language:
                return language
            else:
                return
        except Exception as e:
            raise e