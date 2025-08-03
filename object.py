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
    dp=1,
    minDist=20,
    param1=50,
    param2=30,
    minRadius=5,
    maxRadius=100
)

# Draw circles and crosshair lines
if circles is not None:
    circles = np.uint16(np.around(circles))
    for (x, y, r) in circles[0, :]:
        # Draw circle outline
        cv2.circle(image, (x, y), r, (0, 255, 0), 1)
        # Draw center point
        cv2.circle(image, (x, y), 2, (0, 0, 255), 1)
        
        # Compute extreme points
        top = (x, y - r)
        bottom = (x, y + r)
        left = (x - r, y)
        right = (x + r, y)

        # Draw crosshair lines
        cv2.line(image, (x, y), top, (255, 0, 0), 1)
        cv2.line(image, (x, y), bottom, (255, 0, 0), 1)
        cv2.line(image, (x, y), left, (255, 0, 0), 1)
        cv2.line(image, (x, y), right, (255, 0, 0), 1)

cv2.imshow('Detected Circles with Lines', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
