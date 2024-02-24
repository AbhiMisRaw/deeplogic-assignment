import os
import csv
import pytesseract
from PIL import Image
import fitz
from langdetect import detect
from string import printable
from django.conf import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dataExtractor.settings')

# Specify Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

app = Celery('dataExtractor')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Define utility functions
def is_noise(text):
    return not all(char in printable for char in text)

def detect_eng_language(text):
    known_words = {
        "en": {"invoice", "name", "address", "phone", "product", "total", "date"}
    }
    try:
        detected_lang = detect(text)
        if detected_lang in known_words:
            words = set(text.lower().split())
            valid_words = known_words[detected_lang]
            if any(word in valid_words for word in words):
                return True, detected_lang
    except:
        pass
    return False, None

# Define Celery task
@app.task
def process_text(file_path):
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    try:
        _, file_extension = os.path.splitext(full_path)
        if file_extension.lower() == ".pdf":
            # Extract text from PDF
            text = extract_text_from_pdf(full_path)
        elif file_extension.lower() in [".png", ".jpg", ".jpeg"]:
            # Extract text from image
            text = extract_text_from_image(full_path)
        else:
            return {'status': 'error', 'message': 'Unsupported file format.'}
        
        # Check if the text is noisy or not in English
        if is_noise(text) or not detect_eng_language(text):
            return {'status': 'error', 'message': 'Text is noisy or not in English.'.encode('utf-8')}
        
        # Convert text to CSV
        csv_file_path = os.path.splitext(full_path)[0] + ".csv"
        print(csv_file_path)
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Extracted Text'])
            writer.writerow([text])
        
        return {'status': 'success', 'file_path': f"{os.path.splitext(full_path)[0]+".csv"}" , 'message': 'Hello Text is valid and in English. CSV file created.'.encode('utf-8')}
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return {'status': 'error', 'message': 'Error processing file.'.encode('utf-8')}

# Define text extraction functions
def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image_list = page.get_pixmap()
        img = Image.frombytes("RGB", [image_list.width, image_list.height], image_list.samples)
        text += pytesseract.image_to_string(img)

    return text

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text
