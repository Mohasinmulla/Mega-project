import cv2
import numpy as np

# Load image
image = cv2.imread('cap2.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
gray_blur = cv2.GaussianBlur(gray, (9, 9), 2)

# Detect circles
circles = cv2.HoughCircles(
    gray_blur,
    cv2.HOUGH_GRADIENT,
    dp=1,              # Inverse ratio of resolution
    minDist=20,        # Minimum distance between circle centers
    param1=50,         # Canny edge upper threshold
    param2=30,         # Accumulator threshold for circle detection
    minRadius=5,       # Minimum circle radius in pixels
    maxRadius=100      # Maximum circle radius in pixels
)

# Draw circles
if circles is not None:
    circles = np.uint16(np.around(circles))
    for (x, y, r) in circles[0, :]:
        cv2.circle(image, (x, y), r, (0, 255, 0), 2)
        cv2.circle(image, (x, y), 2, (0, 0, 255), 3)  # Center point

cv2.imshow('Detected Circles', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
