from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
import psutil
import time
from webdriver_manager.chrome import ChromeDriverManager
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
driver.get("https://truyenvipvip.com/cho-anh-mot-co-hoi/chuong-96/")
time.sleep(10)
try:
    button = driver.find_element(By.ID,'readvip')
    
    # Perform actions with the button if needed, for example, click on it
    button.click()

except Exception as e:
    print(f"An error occurred: {e}")
try:
    canvas = driver.find_element(By.ID, "canvas")

    # Lấy kích thước của thẻ canvas
    canvas_width = canvas.size["width"]
    canvas_height = canvas.size["height"]

    # Lấy vị trí của thẻ canvas trên trang
    canvas_location = canvas.location

    # Lấy ảnh từ thẻ canvas
    canvas_screenshot = driver.get_screenshot_as_png()
# Chuyển đổi ảnh tổng thể thành ảnh chỉ chứa phần canvas
    image = Image.open(BytesIO(canvas_screenshot))
    cropped_image = image.crop((canvas_location["x"], canvas_location["y"],
                                canvas_location["x"] + canvas_width, canvas_location["y"] + canvas_height))

    # Lưu ảnh vào một tệp
    cropped_image.save("canvas_screenshot.png")
except Exception as e:
    print(f"An error occurred: {e}")

# Đóng trình duyệt
driver.quit()
