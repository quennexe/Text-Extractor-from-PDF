import json
import os
import fitz
from tkinter import filedialog
import pytesseract
from PIL import Image

# Gerekirse şu satırı aktif et:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def load_language(lang_code):
    lang_path = os.path.join("assets", "lang", f"{lang_code}.json")
    with open(lang_path, "r", encoding="utf-8") as file:
        return json.load(file)

def extract_text(pdf_path, page_range=None, use_ocr=False):
    doc = fitz.open(pdf_path)
    text = ""

    if page_range:
        try:
            start, end = map(int, page_range.split("-"))
            pages = range(start - 1, end)
        except:
            pages = range(len(doc))
    else:
        pages = range(len(doc))

    for i in pages:
        if 0 <= i < len(doc):
            if use_ocr:
                pix = doc[i].get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text += pytesseract.image_to_string(img)
            else:
                text += doc[i].get_text()

    doc.close()
    return text

def save_text_to_file(text):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")],
                                             title="Metni Kaydet")
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)
