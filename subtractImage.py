import cv2
import numpy as np

# Load the two images
image1 = cv2.imread('115380.png')
image2 = cv2.imread('subtract.png')

# Ensure both images have the same dimensions
height, width, channels = image1.shape
image2 = cv2.resize(image2, (width, height))

# Subtract the images
result = cv2.subtract(image1, image2)
threshold = 0  # You can adjust this threshold value
result[result <= threshold] = 255
cv2.imwrite("o.png",result)
# Display the result

cv2.imshow('Subtracted Image', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
