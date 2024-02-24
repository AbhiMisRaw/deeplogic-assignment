from PIL import Image
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import pytesseract
import csv

def detect_eng_language(text):
    known_words = {
        "en": {"invoice", "name", "address", "phone", "product", "total", "date"}
    }

    def is_valid_language(text):
        try:
            detected_lang = detect(text)
            if detected_lang in known_words:
                words = set(text.lower().split())
                valid_words = known_words[detected_lang]
                if any(word in valid_words for word in words):
                    return True, detected_lang
        except LangDetectException:
            pass
        return False, None

    is_valid, detected_language = is_valid_language(text) 

    if is_valid:
        print(f"The text is valid and appears to be in {detected_language}.")
        return True
    else:
        print("The text is not valid or could not be identified as a supported language.")
        return False

def extract_key_value_pairs(text):
    lines = text.split("\n")
    pairs = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            pairs[key.strip()] = value.strip()
    return pairs

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for key, value in data.items():
            writer.writerow([key, value])

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
extracted_text = pytesseract.image_to_string(Image.open('sample1.png'), lang='eng')

if detect_eng_language(extracted_text):
    print("Data is in English language")
    print("------------")
    print(extracted_text)
    print("----------------")
    key_value_pairs = extract_key_value_pairs(extracted_text)
    print("Extracted Key-Value Pairs:")
    for key, value in key_value_pairs.items():
        print(f"{key}: {value}")

    csv_filename = "invoice_data.csv"
    save_to_csv(key_value_pairs, csv_filename)
    print(f"Data saved to {csv_filename}")
else:
    print("Data contains too much noise or is not in English language")
