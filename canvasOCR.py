from selenium import webdriver
import psutil
from selenium.webdriver.common.by import By
import time
root_div_class_name = 'chapter_content'
# Tạo options cho trình duyệt Chrome và đặt đường dẫn profile 
chrome_profile_path = 'C:\\Users\\phamh\\AppData\\Local\\Google\\Chrome\\User Data\\'
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=' + chrome_profile_path)
options.add_argument('--profile-directory=Default')
# Định vị thẻ canvas (thay "myCanvas" bằng id của thẻ canvas thực tế)
for process in psutil.process_iter():
    if process.name() == 'chrome.exe':
        process.kill()
driver = webdriver.Chrome(options=options)
# Set up the WebDriver
driver.get("https://truyenvipvip.com/cung-chieu-co-vo-quan-nhan-11124/chuong-3090/")
try:
        button=driver.find_element(By.ID,"readvip")
        button.click()
        time.sleep(2)
except Exception as e:
        print("don't have button readvip")
# Try getting text from attributes or child elements
root_div_element = driver.find_element(By.CLASS_NAME, root_div_class_name)
canvas_elements = root_div_element.find_elements(By.TAG_NAME, 'canvas')
for index, canvas in enumerate(canvas_elements):
    var context = canvas.getContext("2d");

// Your canvas-specific extraction logic here

// For example, extracting text from the top-left corner
var extractedText = context.getImageData(0, 0, 100, 20);  // Adjust the parameters based on your canvas content
extractedText = extractedText.data.reduce(function(acc, val) {
    return acc + String.fromCharCode(val);
}, '');
    print(canvas_text)
driver.quit()
