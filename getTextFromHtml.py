from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
from io import BytesIO
from PIL import Image
import psutil
from io import BytesIO
import base64
import sys
import os
import re
# Set the path to your web driver
root_div_class_name = 'chapter_content'
# Change the default encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')
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
folderPath=""
# Specify the URL of the website you want to scrape
url = "https://truyenvipvip.com/cung-chieu-co-vo-quan-nhan-11124/chuong-3273/"
def remove_special_characters(input_string):
    pattern = re.compile('[\\:*?"<>|]')
    
    # Use the sub() method to replace matched characters with an empty string
    result_string = re.sub(pattern, '', input_string)
    
    
    return result_string
def getTitle():
    global folderPath
    element=driver.find_element(By.CLASS_NAME,'h3')
    title=element.text
    element = driver.find_element(By.CLASS_NAME, 'size16')
    chuong = element.text
    folderPath=f"{title}/{chuong}"
    folderPath=remove_special_characters(folderPath)
    # folderPath="Cưng Chiều Cô Vợ Quân Nhân full"
    print(folderPath)
    if not os.path.exists(folderPath):
        # Create the folder
        try:
            os.makedirs(folderPath)
            print(f"Folder '{folderPath}' created successfully.")
        except OSError as e:
            print(f"Error creating folder '{folderPath}': {e}")
# Navigate to the website
driver.get(url)
getTitle()
try:
    button=driver.find_element(By.ID,"readvip")
    button.click()
except Exception as e:
    print(f"An error occurred: {e}")
# Extract text from a specific element (e.g., a div with class name 'example-class')
element = driver.find_element(By.CLASS_NAME, 'chapter_content')
time.sleep(3)
text_from_website = element.text
time.sleep(3)
# Print the extracted text
# print("Text from the website:", text_from_website)
paragraphs=text_from_website.split("\n")
# for p in paragraphs:
#     print(f"{p}\n_______________________________________________")
    
time.sleep(100)

# Close the browser
driver.quit()
