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

# Specify the URL of the website you want to scrape
url = "https://truyenvipvip.com/cung-chieu-co-vo-quan-nhan-11124/chuong-3275/"
paragraph=""

# Navigate to the website
driver.get(url)
def cropImage(path,deltaTop,deltaBottom):
    original_image = Image.open(path)
    image_size = original_image.size
    left=0
    right=image_size[0]
    # print(f"image_size:{image_size}")
    bottom=image_size[1]-deltaBottom
    cropped_image = original_image.crop((left, deltaTop, right, bottom))
    cropped_image.save(path)

def ocr_image(image_path):
    # Đọc văn bản từ ảnh sử dụng OCR
    text = pytesseract.image_to_string(Image.open(image_path),lang="vie",config="--psm 6",)
    return text
def remove_prefix_overlap(str1, str2):
    # Độ dài của chuỗi ngắn hơn
    min_len = min(len(str1), len(str2))
    
    # So sánh đầu chuỗi str2 với cuối chuỗi str1
    if str1[-min_len:] == str2[:min_len]:
        return str2[min_len:]
    else:
        return str2
def captureImageFromWebSite(url):
    global driver
    global paragraph
# Mở trang web
    driver.get(url)
    try:
        button=driver.find_element(By.ID,"readvip")
        button.click()
        time.sleep(2)
    except Exception as e:
        print(f"An error occurred: {e}")
    # Định vị thẻ div bạn muốn chụp ảnh
    div_element = driver.find_element(By.CLASS_NAME, "chapter_content")

    # Lấy kích thước của thẻ div
    div_size = div_element.size
    # Lấy kích thước toàn bộ trang web
    total_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    # print(f"total height:{total_height}")
    displayed_height = driver.execute_script("return window.innerHeight;")

    # print(f"displayed_height:{displayed_height}")
    # Scroll and capture multiple screenshots
    location = div_element.location
    # print(f"location['x']:{location['x']}")
    # Scroll and capture screenshots
    for i in range( location['y']-10, total_height, displayed_height-40):
        screenshot_path = f"./scrollCapture/div_screenshot{i}.png"
        driver.execute_script("window.scrollTo(0, {});".format(i))
        time.sleep(1)  # Wait for the content to load
        driver.save_screenshot(screenshot_path)
        next_height=i+displayed_height
        deltaTop=0
        deltaBottom=0
        # print(f"displayed_height:{displayed_height}")
        if next_height>total_height:
            deltaTop=next_height-total_height-60
            chap_button = driver.find_element(By.CLASS_NAME, "bntchap")
            location_button = chap_button.location
            deltaBottom=total_height-location_button['y']+45
            # print(f"deltaTop:{deltaTop}")
            # print(f"deltaBottom:{deltaBottom}")
        cropImage(screenshot_path,deltaTop,deltaBottom)
        text=ocr_image(screenshot_path)
        paragraph+=text
        
    
        
def getText(url):
    driver.get(url)
# Combine the screenshots into a single image
# Thực hiện OCR trên ảnh chụp của thẻ div
# div_text = pytesseract.image_to_string(div_screenshot,lang="vie")
# print("Text extracted from the div:", div_text)
captureImageFromWebSite(url)
# print(paragraph)
paragraphs=paragraph.split("\n\n")
print(paragraph)
# for p in paragraphs:
#     print(f"{p}\n_______________________________________________")
time.sleep(1000)
# Đóng trình duyệt
driver.quit()
