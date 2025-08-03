import cv2
import numpy as np

# Load image
image = cv2.imread('cap2.jpg')
if image is None:
    raise ValueError("Image not found!")

# Calibration: 10 px = 0.1 mm → 1 px = 0.01 mm
px_to_mm = 0.2

# Detect circles
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_blur = cv2.GaussianBlur(gray, (9, 9), 2)

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

display_img = image.copy()
if circles is not None:
    circles = np.uint16(np.around(circles))
    for (x, y, r) in circles[0, :]:
        # Draw circle
        cv2.circle(display_img, (x, y), r, (0, 255, 0), 1)
        cv2.circle(display_img, (x, y), 2, (0, 0, 255), -1)

        # Compute lengths in mm
        length_mm = (2 * r) * px_to_mm

        # Draw horizontal line (with yellow arrow)
        cv2.arrowedLine(display_img, (x-r, y), (x+r, y), (0,255,255), 1, tipLength=0.02)
        # Draw vertical line (with yellow arrow)
        cv2.arrowedLine(display_img, (x, y-r), (x, y+r), (0,255,255), 1, tipLength=0.02)

        # Display text near line ends
        cv2.putText(display_img, f"{length_mm:.2f} mm", (x+r+5, y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 1)
        cv2.putText(display_img, f"{length_mm:.2f} mm", (x, y-r-5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 1)

# Window settings
win_name = "Zoom & Pan with Measurement"
cv2.namedWindow(win_name)

zoom_scale = 1.0
zoom_step = 0.1
offset_x, offset_y = 0, 0
dragging = False
prev_mouse = (0, 0)

def mouse_control(event, x, y, flags, param):
    global zoom_scale, offset_x, offset_y, dragging, prev_mouse

    if event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            zoom_scale += zoom_step
        else:
            zoom_scale = max(1.0, zoom_scale - zoom_step)
    elif event == cv2.EVENT_LBUTTONDOWN:
        dragging = True
        prev_mouse = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        dragging = False
    elif event == cv2.EVENT_MOUSEMOVE and dragging:
        dx = x - prev_mouse[0]
        dy = y - prev_mouse[1]
        offset_x += dx
        offset_y += dy
        prev_mouse = (x, y)

cv2.setMouseCallback(win_name, mouse_control)

h, w = display_img.shape[:2]

while True:
    # Zoomed image
    zoomed_w, zoomed_h = int(w * zoom_scale), int(h * zoom_scale)
    zoomed_img = cv2.resize(display_img, (zoomed_w, zoomed_h), interpolation=cv2.INTER_CUBIC)

    # Compute view window
    view_w, view_h = w, h
    start_x = int((zoomed_w - view_w) / 2 - offset_x)
    start_y = int((zoomed_h - view_h) / 2 - offset_y)

    # Ensure within bounds
    start_x = max(0, min(start_x, zoomed_w - view_w))
    start_y = max(0, min(start_y, zoomed_h - view_h))

    view = zoomed_img[start_y:start_y + view_h, start_x:start_x + view_w]

    cv2.imshow(win_name, view)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC to exit
        break

cv2.destroyAllWindows()
