import numpy as np
import cv2

def remove_small_text(img):
  """
  Loại bỏ các chữ nhỏ màu đen nhạt đè lên chữ đen trong ảnh.

  Args:
      img: Ảnh đầu vào (mảng NumPy).

  Returns:
      Ảnh sau khi loại bỏ (mảng NumPy).
  """

  # Chuyển đổi ảnh sang ảnh xám
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  print(gray)

  # Áp dụng ngưỡng
  thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

  # Lấp đầy các vùng nhỏ
  kernel = np.ones((3,3), np.uint8)
  closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

  # Chuyển đổi ảnh trở lại thang màu RGB
  result = cv2.cvtColor(closed, cv2.COLOR_GRAY2BGR)

  return result

# Đọc ảnh
img = cv2.imread("121108.png")

# Loại bỏ chữ nhỏ
result = remove_small_text(img)

# Hiển thị kết quả
cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
