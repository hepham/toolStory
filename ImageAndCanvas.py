from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
from io import BytesIO
from PIL import Image
import psutil
from io import BytesIO
import base64
# Set the path to your web driver
url = 'https://truyenvipvip.com/cung-chieu-co-vo-quan-nhan-11124/chuong-3273/'
root_div_class_name = 'chapter_content'

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
count=0
# Open the website
def capture_canvas_screenshots_within_div(div_element):
    global count
    # Capture screenshots of all canvas elements within the current div
    print("_________________")
    print(f'element:{div_element.get_attribute("class")}')
    canvas_elements = div_element.find_elements(By.TAG_NAME, 'canvas')
    for index, canvas in enumerate(canvas_elements):
        print(map)
        print("***********")
        print(f'div element:{div_element.get_attribute("class")}')
        # Scroll to the canvas element to make sure it's in the viewport
        driver.execute_script("arguments[0].scrollIntoView();", canvas)
        time.sleep(1)  # Wait for any potential dynamic content to load
        # print(canvas_elements)
        # # Capture screenshot of the canvas element
        canvas_screenshot = canvas.screenshot_as_png
    
        # Save the screenshot to a file
        with open(f"canvas_screenshot_{count + 1}.png", "wb") as file:
            file.write(canvas_screenshot)
            count+=1
    # Recursively process nested divs
    nested_divs = div_element.find_elements(By.TAG_NAME, 'span')
    for nested_div in nested_divs:
        print(f'nested div:{nested_div.get_attribute("class")} in span')
        capture_canvas_screenshots_within_div(nested_div,map)
    nested_divs = div_element.find_elements(By.TAG_NAME, 'div')
    for nested_div in nested_divs:
        print(f'nested div:{nested_div.get_attribute("class")} in div')
        capture_canvas_screenshots_within_div(nested_div,map)

# Open the website
driver.get(url)

# Wait for the page to load (you might need to adjust the time)
time.sleep(3)
try:
    button=driver.find_element(By.ID,"readvip")
    button.click()
except Exception as e:
    print(f"An error occurred: {e}")
# Find the root div element with the specified class name
root_div_element = driver.find_element(By.CLASS_NAME, root_div_class_name)
# Start capturing canvas screenshots within the root div
capture_canvas_screenshots_within_div(root_div_element)

print("Canvas screenshots captured successfully!")

# Download all images within the root div
img_elements = root_div_element.find_elements(By.TAG_NAME, 'img')

for index, img in enumerate(img_elements):
    # Get the image source URL
    img_url = img.get_attribute('src')
    try:
    # Download the image
        response = requests.get(img_url)
        img_data = BytesIO(response.content)

        # Save the image to a file
        with Image.open(img_data) as img_file:
            img_file.save(f"image_{index + 1}.png")
    except Exception as e:
        print(f"An error occurred: {e}")
        

# print("Images downloaded successfully!")
time.sleep(1000)
# Close the WebDriver
driver.quit()