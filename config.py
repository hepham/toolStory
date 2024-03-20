import sys
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By
# Change the default encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')
# Cài đặt đường dẫn tới tesseract.exe (nếu cần)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Khởi tạo trình duyệt (sử dụng ChromeDriver)
root_div_class_name = 'chapter_content'
# Change the default encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')
# Khởi tạo trình duyệt (Chrome, Firefox, hoặc trình duyệt khác)
chrome_profile_path = 'C:\\Users\\phamh\\AppData\\Local\\Google\\Chrome\\User Data\\'


# Tạo options cho trình duyệt Chrome và đặt đường dẫn profile
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=' + chrome_profile_path)
options.add_argument('--profile-directory=Default')
# Định vị thẻ canvas (thay "myCanvas" bằng id của thẻ canvas thực tế)
for process in psutil.process_iter():
    if process.name() == 'chrome.exe':
        process.kill()
driver = webdriver.Chrome(options=options)