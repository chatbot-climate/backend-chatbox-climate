from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from langdetect import detect



translator_to_en = pipeline("translation", model="Helsinki-NLP/opus-mt-mul-en") # Chargement du modèle de traduction multilingue -> anglais
summarizer = pipeline("summarization", model="facebook/bart-large-cnn") # Exemple de modèle de traitement


def get_back_translator(lang_code):
    
    try:
        return pipeline("translation", model=f"Helsinki-NLP/opus-mt-en-{lang_code}")
    except Exception as exc:
        raise ValueError(f"Langue non prise en charge pour la retraduction: {lang_code}")

    # model_map = {
    #     "en": "Helsinki-NLP/opus-mt-fr-en",
    #     "es": "Helsinki-NLP/opus-mt-fr-es",
    #     "de": "Helsinki-NLP/opus-mt-fr-de",
    #     "sw": "Helsinki-NLP/opus-mt-fr-swa",
    #     "pt": "Helsinki-NLP/opus-mt-fr-pt",
    # }

    # model_map = {
    #     "fr": "Helsinki-NLP/opus-mt-en-fr",
    #     "en": "Helsinki-NLP/opus-mt-mul-en",
    #     "es": "Helsinki-NLP/opus-mt-en-es",
    #     "de": "Helsinki-NLP/opus-mt-en-de",
    #     "sw": "Helsinki-NLP/opus-mt-en-swa",
    #     "pt": "Helsinki-NLP/opus-mt-en-pt",
    # }
    # if lang_code not in model_map:
    #     raise ValueError(f"Langue non prise en charge pour la retraduction: {lang_code}")
    # return pipeline("translation", model=model_map[lang_code])


def detect_language(text):
    return detect(text)


def translate_and_summarize_in_en(text):
    lang = detect_language(text)
    if lang != 'en':
        print(f"Texte détecté en '{lang}', traduction vers l'anglais...")
        translated = translator_to_en(text)[0]['translation_text']
    else:
        translated = text

    result = summarizer(translated, max_length=100, min_length=30, do_sample=False) # Traitement du texte (résumé ici)

    return translated, result[0]['summary_text'], lang



def translate_en_text_in_multilang(text_en, original_lang):
    result = summarizer(text_en, max_length=60, min_length=20, do_sample=False)[0]["summary_text"] # Faire un résumé ou autre traitement
    
    back_translator = get_back_translator(original_lang) # Traduire le résultat en langue d’origine
    translated_back = back_translator(result)[0]["translation_text"]

    return translated_back