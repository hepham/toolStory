from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
import time
import sys
import psutil
# Change the default encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')
# Cài đặt đường dẫn tới tesseract.exe (nếu cần)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Khởi tạo trình duyệt (sử dụng ChromeDriver)
root_div_class_name = 'chapter_content'
# Change the default encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')
def ocr_image(image_path):
    # Đọc văn bản từ ảnh sử dụng OCR
    text = pytesseract.image_to_string(Image.open(image_path),lang="vie",config="--psm 6",).split("\n")
    for t in text:
        print("***********")
        print(t)

    # print(text)
    return text
ocr_image("Cưng Chiều Cô Vợ Quân Nhân full\Chương 1 Sống lại thành tân binh (1)\images\image_1.png")