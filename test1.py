from selenium import webdriver
from selenium.webdriver.common.by import By
# Initialize the webdriver
driver = webdriver.Chrome()

# Open the webpage
driver.get("https://hentai18vn.net/truyen-hentai/shinkansen-de-nani-shiteru/part-01-ch1537")

# Find the button element by its XPath, CSS selector, or any other locating strategy
button = driver.find_element(By.CLASS_NAME,"btn.btn-success.btn-chapter-next")

# Get the URL from the button
button_url = button.get_attribute("href")

# Print the URL
print("Button URL:", button_url)

# Close the webdriver
driver.quit()
