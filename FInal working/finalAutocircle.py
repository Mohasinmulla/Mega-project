import cv2
import numpy as np
import math

# ----------------------------
# User parameters
# ----------------------------
pixel_per_mm = 101  # ← Enter pixel-per-mm from calibration
image_path = '214_HBW.jpg'

# ----------------------------
# Step 1: Load and preprocess
# ----------------------------
img = cv2.imread(image_path)
orig = img.copy()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 9, 75, 75)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
gray = clahe.apply(gray)

# ----------------------------
# Step 2: Remove glare
# ----------------------------
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
gray_corr = cv2.subtract(gray, tophat)

# ----------------------------
# Step 3: Threshold
# ----------------------------
thresh = cv2.adaptiveThreshold(
    gray_corr, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV, 15, 4
)

# ----------------------------
# Step 4: Contour-based circle detection
# ----------------------------
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

best_circle = None
for c in contours:
    area = cv2.contourArea(c)
    if area < 50:
        continue
    perimeter = cv2.arcLength(c, True)
    if perimeter == 0:
        continue
    circularity = (4 * np.pi * area) / (perimeter * perimeter)

    if 0.75 < circularity < 1.25:
        (x, y), radius = cv2.minEnclosingCircle(c)
        if 5 < radius < 100:
            best_circle = (int(x), int(y), int(radius))
            cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 0), 1)
            cv2.circle(img, (int(x), int(y)), 2, (0, 0, 255), 1)
            break

# ----------------------------
# Step 5: Fallback to HoughCircles
# ----------------------------
if best_circle is None:
    circles = cv2.HoughCircles(
        gray_corr,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=50,
        param1=80,
        param2=20,
        minRadius=5,
        maxRadius=100
    )
    if circles is not None:
        circles = np.uint16(np.around(circles))
        x, y, r = circles[0, 0]
        best_circle = (int(x), int(y), int(r))
        cv2.circle(img, (x, y), r, (255, 0, 0), 1)
        cv2.circle(img, (x, y), 2, (0, 0, 255), 1)

# ----------------------------
# Step 6: Output detection
# ----------------------------
if best_circle is not None:
    x, y, r = best_circle
    diameter_px = 2 * r
    print("\n✅ Circle Detected:")
    print(f"  Center: ({x}, {y})")
    print(f"  Radius: {r} px")
    print(f"  Diameter: {diameter_px} px")
else:
    print("❌ No circle detected.")
    exit()

# ----------------------------
# Show detected circle
# ----------------------------
cv2.imshow("Detected Circle", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ----------------------------
# Convert pixels → mm
# ----------------------------
d_mm = diameter_px / pixel_per_mm
print(f"\n📏 Indentation diameter = {d_mm:.2f} mm")

# ----------------------------
# Step 7: HBW Calculation
# ----------------------------
def calculate_HBW(P, D, d):
    numerator = 2 * P
    denominator = math.pi * D * (D - math.sqrt(D**2 - d**2))
    HBW = numerator / denominator
    return HBW


# User selects test conditions
choice = int(input(
    "\nSelect Brinell Test:\n"
    "1 - Load = 750 kg,  Ball = 5 mm\n"
    "2 - Load = 3000 kg, Ball = 10 mm\n"
    "3 - Load = 1000 kg, Ball = 10 mm\n"
    "Enter choice: "
))

match choice:
    case 1:
        P = 750
        D = 5
    case 2:
        P = 3000
        D = 10
    case 3:
        P = 1000
        D = 10
    case _:
        print("Invalid choice")
        exit()

hbw_value = calculate_HBW(P, D, d_mm)
final_hbw_value = round(hbw_value)

print("\n✅ Final Results:")
print(f"Indentation d = {d_mm:.2f} mm")
print(f"Brinell Hardness Number (HBW) = {final_hbw_value}\n")

