import cv2
import numpy as np

# -------------- SETTINGS ------------------
image_path = "ruler.jpg"
ref_length_mm = 1.0
NUM_REF_MEASUREMENTS = 10

pixel_per_mm = None
freeze_mode = None
freeze_value = None

prev_point = None
measurements_px = []

# -------------- LOAD ------------------
image = cv2.imread(image_path)
if image is None:
    raise ValueError("Image not found!")

clone = image.copy()

# -------------- HELPERS ------------------
def draw_freeze_line(img):
    if freeze_mode == "H" and freeze_value is not None:
        cv2.line(img, (0, freeze_value), (img.shape[1], freeze_value), (0, 255, 255), 1)

def draw_point(img, p):
    x, y = p
    cv2.circle(img, (x, y), 3, (0, 0, 255), -1)

def draw_horizontal_marker(img, p):
    """ Draw 50px horizontal line centered at point """
    x, y = p
    cv2.line(img, (x - 25, y), (x + 25, y), (255, 0, 255), 1)

def measure_distance(p1, p2):
    return abs(p2[0] - p1[0])  # horizontal distance only


# -------------- MOUSE CALLBACK ------------------
def mouse_callback(event, mx, my, flags, param):
    global clone, freeze_value, prev_point, pixel_per_mm, measurements_px, freeze_mode

    if event == cv2.EVENT_MOUSEMOVE:
        temp = clone.copy()
        draw_freeze_line(temp)
        cv2.imshow("Image", temp)
        return

    if event == cv2.EVENT_LBUTTONDOWN:

        # ----------------------------
        # FIRST CLICK → AUTO-FREEZE HORIZONTAL
        # ----------------------------
        if prev_point is None:
            freeze_mode = "H"       # freeze Y axis
            freeze_value = my       # freeze Y coordinate
            p = (mx, freeze_value)

            draw_point(clone, p)
            draw_horizontal_marker(clone, p)
            draw_freeze_line(clone)

            prev_point = p
            cv2.imshow("Image", clone)
            return

        # ----------------------------
        # NEXT CLICKS
        # snap Y to frozen value
        # ----------------------------
        p = (mx, freeze_value)

        draw_point(clone, p)
        draw_horizontal_marker(clone, p)

        p1 = prev_point
        p2 = p

        # draw measurement segment
        cv2.line(clone, p1, p2, (0, 255, 0), 1)

        dist_px = measure_distance(p1, p2)
        print(f"Distance px = {dist_px:.2f}")

        # ---- CALIBRATION ----
        if pixel_per_mm is None:
            measurements_px.append(dist_px)
            print(f"[{len(measurements_px)}/{NUM_REF_MEASUREMENTS}]")

            if len(measurements_px) == NUM_REF_MEASUREMENTS:
                avg_px = sum(measurements_px) / NUM_REF_MEASUREMENTS
                pixel_per_mm = avg_px / ref_length_mm
                print("\n✅ Calibration completed!")
                print(f"Pixel per mm = {pixel_per_mm:.3f}")

        # ---- NORMAL MEASUREMENT ----
        else:
            real_mm = dist_px / pixel_per_mm
            print(f"Measured = {real_mm:.2f} mm")

            cv2.putText(clone, f"{real_mm:.2f} mm",
                        (p2[0] + 5, p2[1] - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (255, 0, 0), 2)

        prev_point = p
        draw_freeze_line(clone)
        cv2.imshow("Image", clone)



# -------------- MAIN LOOP ------------------
cv2.imshow("Image", clone)
cv2.setMouseCallback("Image", mouse_callback)

print("\n✅ Instructions")
print("• First click = freeze Y axis automatically")
print("• Horizontal freeze line appears")
print("• Every next click snaps to same horizontal line")
print("• 50px horizontal marker drawn on each point\n")

while True:
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
