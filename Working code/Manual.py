import cv2
import numpy as np
import math
import os
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================
IMAGE_PATH = r"C:\Users\Admin\Desktop\Projects\Opencv\Images\214_HBW.jpg"
SAVE_FOLDER = r"C:\Users\Admin\Desktop\Projects\Opencv\Results"

pixel_per_mm = 166     # Set None for calibration mode
ref_length_mm = 1.0

points = []
final_measured_mm = None
final_measure_img = None

# ============================================================
# LOAD IMAGE
# ============================================================
image = cv2.imread(IMAGE_PATH)
if image is None:
    raise ValueError("Image not found!")

clone = image.copy()


# ============================================================
# MOUSE CALLBACK (Optimized & Clean)
# ============================================================
def mouse_callback(event, x, y, flags, param):
    global points, clone, pixel_per_mm, final_measured_mm, final_measure_img

    # Crosshair on mouse move
    if event == cv2.EVENT_MOUSEMOVE:
        temp = clone.copy()
        cv2.line(temp, (0, y), (temp.shape[1], y), (200, 200, 200), 1)
        cv2.line(temp, (x, 0), (x, temp.shape[0]), (200, 200, 200), 1)
        cv2.imshow("Image", temp)

    # Left Click
    elif event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))

        # First click
        if len(points) % 2 == 1:
            cv2.circle(clone, (x, y), 2, (0, 0, 255), -1)

        # Second click
        else:
            x1, y1 = points[-2]
            x2 = x
            y2 = y1
            points[-1] = (x2, y2)

            # Draw on screen-only clone
            cv2.circle(clone, (x2, y2), 2, (0, 0, 255), -1)
            cv2.line(clone, (x1, y1), (x2, y2), (0, 255, 0), 1)

            # Pixel distance (horizontal only)
            dist_px = abs(x2 - x1)
            print(f"\nPixel Distance: {dist_px:.2f} px")

            # -----------------------------
            # ✅ CLEAN FINAL MEASUREMENT IMG
            # -----------------------------
            final_measure_img = image.copy()
            cv2.circle(final_measure_img, (x1, y1), 2, (0, 0, 255), -1)
            cv2.circle(final_measure_img, (x2, y2), 2, (0, 0, 255), -1)
            cv2.line(final_measure_img, (x1, y1), (x2, y2), (0, 255, 0), 1)

            # Calibration Mode
            if pixel_per_mm is None:
                pixel_per_mm = dist_px / ref_length_mm
                print(f"Calculated Pixel-per-mm = {pixel_per_mm:.2f}")
                cv2.putText(clone, f"Ref {ref_length_mm}mm",
                          (x2, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                cv2.putText(final_measure_img, f"Ref {ref_length_mm}mm",
                          (x2, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            else:
                real_mm = dist_px / pixel_per_mm
                final_measured_mm = real_mm
                print(f"Measured Distance = {real_mm:.2f} mm")
                cv2.putText(clone, f"{real_mm:.2f} mm",
                          (x2, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                cv2.putText(final_measure_img, f"{real_mm:.2f} mm",
                          (x2, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        cv2.imshow("Image", clone)


# ============================================================
# SETUP GUI
# ============================================================
cv2.imshow("Image", clone)
cv2.setMouseCallback("Image", mouse_callback)

print("\nClick 2 points on indentation diameter.")
print("Press 'r' to reset, 'Enter' to proceed.\n")

# ============================================================
# MAIN INTERACTION LOOP
# ============================================================
while True:
    key = cv2.waitKey(1)

    if key == ord('r'):
        points.clear()
        clone = image.copy()
        final_measure_img = None
        final_measured_mm = None
        print("Points reset.\n")
        cv2.imshow("Image", clone)

    elif key == 13:  # ENTER key
        if final_measured_mm is not None:
            break
        print("❗Measure distance first before pressing Enter.\n")


# ============================================================
# BRINELL HARDNESS CALCULATION
# ============================================================
def calculate_HBW(P, D, d):
    numerator = 2 * P
    denominator = math.pi * D * (D - math.sqrt(D * D - d * d))
    return numerator / denominator


d_mm = final_measured_mm
print(f"\nMeasured indentation (d): {d_mm:.2f} mm")


# ============================================================
# TEST TYPE SELECTION UI
# ============================================================
img_display = final_measure_img.copy()
cv2.putText(img_display, f"Diameter: {d_mm:.2f} mm",
            (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

# Close the first image window
cv2.destroyWindow("Image")

# Instructions
instructions = [
    "Select Brinell Test:",
    "Press 1 -> Load 750 kg, Ball 5 mm",
    "Press 2 -> Load 3000 kg, Ball 10 mm",
    "Press 3 -> Load 1000 kg, Ball 10 mm",
]

y = 70
for line in instructions:
    cv2.putText(img_display, line, (20, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    y += 30

cv2.imshow("HBW Calculator", img_display)

# Get test selection
P = None
D = None
while True:
    key = cv2.waitKey(0)
    if key == ord('1'):
        P, D = 750, 5
        break
    elif key == ord('2'):
        P, D = 3000, 10
        break
    elif key == ord('3'):
        P, D = 1000, 10
        break


# ============================================================
# FINAL HBW OUTPUT SCREEN
# ============================================================
HBW = round(calculate_HBW(P, D, d_mm))

final_img = final_measure_img.copy()
cv2.putText(final_img, f"Diameter: {d_mm:.2f} mm",
            (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
cv2.putText(final_img, f"HBW = {HBW}",
            (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

cv2.imshow("HBW Calculator", final_img)
cv2.waitKey(500)


# ============================================================
# SAVE OUTPUT IMAGE AUTOMATICALLY
# ============================================================
os.makedirs(SAVE_FOLDER, exist_ok=True)
timestamp = datetime.now().strftime("%d-%m-%y_%H-%M")
save_path = os.path.join(SAVE_FOLDER, f"{timestamp}_HBW-{HBW}.jpg")

cv2.imwrite(save_path, final_img)
print(f"\n✅ Saved at: {save_path}\n")

cv2.waitKey(0)
cv2.destroyAllWindows()
