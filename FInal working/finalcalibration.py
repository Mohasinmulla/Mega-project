import cv2
import numpy as np
import math

# -----------------------------
#  Part 1: Distance Measurement
# -----------------------------

image_path = '218_2_HBW.jpg'
image = cv2.imread(image_path)

if image is None:
    raise ValueError("Image not found!")

clone = image.copy()
points = []

# Set this to None if you want first two clicks to calibrate pixel-per-mm
pixel_per_mm = None    # <-- set to None for calibration mode
ref_length_mm = 1.0    # reference length (mm)


def mouse_callback(event, x, y, flags, param):
    global points, clone, pixel_per_mm, final_measured_mm

    # Show dynamic crosshair
    if event == cv2.EVENT_MOUSEMOVE:
        temp = clone.copy()
        cv2.line(temp, (0, y), (temp.shape[1], y), (200, 200, 200), 1)
        cv2.line(temp, (x, 0), (x, temp.shape[0]), (200, 200, 200), 1)
        cv2.imshow("Image", temp)

    elif event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))

        # Odd click → first point
        if len(points) % 2 == 1:
            cv2.circle(clone, (x, y), 2, (0, 0, 255), -1)

        # Even click → second point
        else:
            x1, y1 = points[-2]
            x2, _ = x, y1     # horizontal measurement
            points[-1] = (x2, y1)

            cv2.circle(clone, (x2, y1), 2, (0, 0, 255), -1)
            cv2.line(clone, (x1, y1), (x2, y1), (0, 255, 0), 1)

            # Pixel distance
            dist_px = abs(x2 - x1)
            print(f"\nPixel Distance: {dist_px:.2f} px")

            # Calibration mode
            if pixel_per_mm is None:
                pixel_per_mm = dist_px / ref_length_mm
                print(f"Calculated Pixel-per-mm = {pixel_per_mm:.2f}")
                cv2.putText(clone, f"Ref {ref_length_mm}mm",
                            (x2, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)

            else:
                # Convert pixels → mm
                real_mm = dist_px / pixel_per_mm
                final_measured_mm = real_mm  # store value globally

                print(f"Measured Distance = {real_mm:.2f} mm")
                cv2.putText(clone, f"{real_mm:.2f} mm",
                            (x2, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)

        cv2.imshow("Image", clone)


# Start GUI
cv2.imshow("Image", clone)
cv2.setMouseCallback("Image", mouse_callback)

print("Click 2 points on indentation diameter to measure d in mm...\n")
cv2.waitKey(0)
cv2.destroyAllWindows()

# -------------------------------------
#  Part 2: Brinell Hardness Calculation
# -------------------------------------

def calculate_HBW(P, D, d):
    numerator = 2 * P
    denominator = math.pi * D * (D - math.sqrt(D**2 - d**2))
    HBW = numerator / denominator
    return HBW

# Use measured d
try:
    d = final_measured_mm
except:
    raise ValueError("You did not measure distance properly!")

print("\nMeasured indentation diameter (d): {:.2f} mm".format(d))

# Test type selection
choice = int(input(
    "\nSelect Brinell Test Option:\n"
    "1 - Load = 750 kg, Ball = 5 mm\n"
    "2 - Load = 1000 kg, Ball = 10 mm\n"
    "3 - Load = 3000 kg, Ball = 10 mm\n"
    "Enter choice: "
))

match choice:
    case 1:
        P = 750
        D = 5
    case 2:
        P = 1000
        D = 10
    case 3:
        P = 3000
        D = 10
    case _:
        print("Invalid choice!")
        exit()

# Calculate hardness
hbw_value = calculate_HBW(P, D, d)
final_hbw_value = round(hbw_value)

# Output
print("\n------ RESULTS ------")
print(f"Measured d = {d:.2f} mm")
print(f"Brinell Hardness (HBW) = {final_hbw_value}")
print("---------------------\n")
