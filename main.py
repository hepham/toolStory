from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
import time
import sys
import psutil
import re
import os
import requests
from io import BytesIO
import imagehash
import Levenshtein
from AnotherCalculateSimilar import *
from sklearn.feature_extraction.text import CountVectorizer
ocrCanvasText={}
ocrCanvasCheck={}
saveString=""
textInImages=[]
# Change the default encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')
# Cài đặt đường dẫn tới tesseract.exe (nếu cần)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Khởi tạo trình duyệt (sử dụng ChromeDriver)
root_div_class_name = 'chapter_content'
# Change the default encoding to UTF-8
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
def cropImage(path,deltaTop,deltaBottom):
    # print(path)
    original_image = Image.open(path)
    image_size = original_image.size
    left=0
    right=image_size[0]
    # print(f"image_size:{image_size}")
    bottom=image_size[1]-deltaBottom
    cropped_image = original_image.crop((left, deltaTop, right, bottom))
    cropped_image.save(path)

def calculate_hash(image_path):
    with Image.open(image_path) as img:
        # Resize the image to a fixed size for consistency
        # Convert the image to grayscale
        grayscale_img = img.convert('L')
        # Calculate the perceptual hash
        return imagehash.average_hash(grayscale_img)

def find_and_remove_duplicates(folder_path):
    hash_dict = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(folder_path, filename)
            image_hash = calculate_hash(file_path)

            # Check if the hash already exists (duplicate)
            if image_hash in hash_dict:
                # print(f"Removing duplicate: {filename}")
                os.remove(file_path)
            else:
                # Store the hash in the dictionary
                hash_dict[image_hash] = file_path
def ocr_image(image_path):
    # Đọc văn bản từ ảnh sử dụng OCR
    text = pytesseract.image_to_string(Image.open(image_path),lang="vie",config="--psm 6",)
    return text
def remove_special_characters(input_string):
    pattern = re.compile('[\\:*?"<>|]')
    
    # Use the sub() method to replace matched characters with an empty string
    result_string = re.sub(pattern, '', input_string)
    return result_string
def remove_prefix_overlap(str1, str2):
    # Độ dài của chuỗi ngắn hơn
    min_len = min(len(str1), len(str2))
    
    # So sánh đầu chuỗi str2 với cuối chuỗi str1
    if str1[-min_len:] == str2[:min_len]:
        return str2[min_len:]
    else:
        return str2
def captureImageFromWebSite(url):
    global driver,paragraph,folderPath
# Mở trang web
    driver.get(url)
    try:
        button=driver.find_element(By.ID,"readvip")
        button.click()
        time.sleep(2)
    except Exception as e:
        print("don't have button readvip")
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
        screenshot_path = f"{folderPath}/scrollCapture/div_screenshot{i}.png"
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
def getTitle():
    element=driver.find_element(By.CLASS_NAME,'h3')
    title=element.text
    element = driver.find_element(By.CLASS_NAME, 'size16')
    chuong = element.text
    folderPath=f"{title}/{chuong}"
    folderPath=remove_special_characters(folderPath)
    # folderPath="Cưng Chiều Cô Vợ Quân Nhân full"
    # print(folderPath)
    if not os.path.exists(folderPath):
        # Create the folder
        try:
            os.makedirs(folderPath)
            canvasFolder=f"{folderPath}/canvas"
            os.makedirs(canvasFolder)
            imageFolder=f"{folderPath}/images"
            os.makedirs(imageFolder)
            # print(f"Folder '{canvasFolder}' created successfully.")
        except OSError as e:
            pass
    canvasFolder=f"{folderPath}/canvas"
    if not os.path.exists(canvasFolder):
        # Create the folder
        try:
            os.makedirs(canvasFolder)
            # print(f"Folder '{canvasFolder}' created successfully.")
        except OSError as e:
            pass
    imageFolder=f"{folderPath}/images"
    if not os.path.exists(imageFolder):
        # Create the folder
        try:
            os.makedirs(imageFolder)
            # print(f"Folder '{imageFolder}' created successfully.")
        except OSError as e:
            pass
    scrollCaptureFolder=f"{folderPath}/scrollCapture"
    if not os.path.exists(scrollCaptureFolder):
        # Create the folder
        try:
            os.makedirs(scrollCaptureFolder)
            # print(f"Folder '{scrollCaptureFolder}' created successfully.")
        except OSError as e:
            pass
    return folderPath
# Navigate to the website
def getText(index):
    global folderPath
    try:
        button=driver.find_element(By.ID,"readvip")
        button.click()
    except Exception as e:
       pass
    # Extract text from a specific element (e.g., a div with class name 'example-class')
    element = driver.find_element(By.CLASS_NAME, 'chapter_content')
    time.sleep(1)
    text_from_website = element.text.replace("ℓ","l")
    filetxtName=f"{folderPath}/textCrawl{index}.txt"
    with open(filetxtName,"w",encoding="utf-8") as file:
        file.write(text_from_website)
        file.close()
    # Print the extracted text
    # print("Text from the website:", text_from_website)
    # textFileName=f"{folderPath}/"
# for p in paragraphs:
#     print(f"{p}\n_______________________________________________")
    

# Combine the screenshots into a single image
# Thực hiện OCR trên ảnh chụp của thẻ div
# div_text = pytesseract.image_to_string(div_screenshot,lang="vie")
# print("Text extracted from the div:", div_text)
def capture_canvas_screenshots_within_div(div_element):
    count=0
    # Capture screenshots of all canvas elements within the current div
    # print(f'element:{div_element.get_attribute("class")}')
    canvas_elements = div_element.find_elements(By.TAG_NAME, 'canvas')
    for index, canvas in enumerate(canvas_elements):
        # print(f'div element:{div_element.get_attribute("class")} {index}')
        # Scroll to the canvas element to make sure it's in the viewport
        parent_element = canvas.find_element(By.XPATH,'..')
        # print(parent_element.text)
        driver.execute_script("arguments[0].scrollIntoView();", canvas)
        time.sleep(1)  # Wait for any potential dynamic content to load
        # print(canvas_elements)
        # # Capture screenshot of the canvas element
        canvas_screenshot = canvas.screenshot_as_png
    
        # Save the screenshot to a file
        with open(f"{folderPath}/canvas/canvas_screenshot_{count + 1}.png", "wb") as file:
            file.write(canvas_screenshot)
            count+=1
    # Recursively process nested divs
    # nested_divs = div_element.find_elements(By.TAG_NAME, 'span')
    # for nested_div in nested_divs:
    #     capture_canvas_screenshots_within_div(nested_div)
    # nested_divs = div_element.find_elements(By.TAG_NAME, 'div')
    # for nested_div in nested_divs:
    #     capture_canvas_screenshots_within_div(nested_div)
    
    # print("Canvas screenshots captured successfully!")

def getImageFromWebsite():
    root_div_element = driver.find_element(By.CLASS_NAME, root_div_class_name)
    img_elements = root_div_element.find_elements(By.TAG_NAME, 'img')
    # Download all images within the root div
    for index, img in enumerate(img_elements):
        # Get the image source URL
        img_url = img.get_attribute('src')
        try:
        # Download the image
            response = requests.get(img_url)
            img_data = BytesIO(response.content)

            # Save the image to a file
            with Image.open(img_data) as img_file:
                img_file.save(f"{folderPath}/images/image_{index + 1}.png")
        except Exception as e:
            pass
def getImage():
     # Find the root div element with the specified class name
    root_div_element = driver.find_element(By.CLASS_NAME, root_div_class_name)
    # Start capturing canvas screenshots within the root div
    capture_canvas_screenshots_within_div(root_div_element)
    getImageFromWebsite()
    folder_path = f"{folderPath}/canvas"
    find_and_remove_duplicates(folder_path)
def crawlData(url):    
    global folderPath,paragraph
    # Navigate to the website
    driver.get(url)
    folderPath= getTitle()    
    paragraph=""
    captureImageFromWebSite(url)
    getImage()
    
    for i in range(0,5):
        driver.refresh() 
        getText(i)
    filetxtName=f"{folderPath}/screenshotText.txt"
    with open(filetxtName,"w",encoding="utf-8") as file:
        file.write(paragraph)
        file.close()
    sortText(folderPath)
    
# Main function
prefix="https://truyenvipvip.com/cung-chieu-co-vo-quan-nhan-11124"
for i in range(3090,3200):
    url=f"{prefix}/chuong-{i}"
    crawlData(url)
# print(paragraph)
# paragraphs=paragraph.split("\n\n")
# print(paragraph)
# for p in paragraphs:
#     print(f"{p}\n_______________________________________________")
# time.sleep(1000)
# Đóng trình duyệt
driver.quit()
