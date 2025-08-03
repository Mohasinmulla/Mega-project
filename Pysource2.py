import cv2
import numpy as np

# --- Global Variables ---
points = []          # Store selected points
zoom = 1.0           # Current zoom level
pan_x, pan_y = 0, 0  # Panning offsets
dragging = False
last_mouse_pos = None

# Load the image
image = cv2.imread("cap2.jpg")  # Change this to your image
if image is None:
    raise ValueError("Image not found!")

image_h, image_w = image.shape[:2]

def draw_overlay(img):
    """Draw points and lines if 4 points are selected."""
    temp = img.copy()
    if len(points) == 4:
        x1, _ = points[0]
        x2, _ = points[1]
        _, y1 = points[2]
        _, y2 = points[3]

        # Draw vertical lines
        cv2.line(temp, (x1, 0), (x1, temp.shape[0]), (0, 255, 0), 1)
        cv2.line(temp, (x2, 0), (x2, temp.shape[0]), (0, 255, 0), 1)

        # Draw horizontal lines
        cv2.line(temp, (0, y1), (temp.shape[1], y1), (0, 255, 0), 1)
        cv2.line(temp, (0, y2), (temp.shape[1], y2), (0, 255, 0), 1)

    # Draw red points
    for p in points:
        cv2.circle(temp, p, 1, (0, 0, 255), -1)

    return temp

def apply_zoom_and_pan(img):
    """Apply zoom and pan to image."""
    global zoom, pan_x, pan_y
    h, w = img.shape[:2]
    scaled = cv2.resize(img, (int(w * zoom), int(h * zoom)))

    # Calculate visible region
    view_w, view_h = w, h
    max_x = max(0, scaled.shape[1] - view_w)
    max_y = max(0, scaled.shape[0] - view_h)

    pan_x_clamped = max(0, min(pan_x, max_x))
    pan_y_clamped = max(0, min(pan_y, max_y))

    return scaled[pan_y_clamped:pan_y_clamped+view_h,
                  pan_x_clamped:pan_x_clamped+view_w]

def mouse_event(event, x, y, flags, param):
    global points, dragging, last_mouse_pos, pan_x, pan_y, zoom

    if event == cv2.EVENT_LBUTTONDOWN:
        # Transform screen coords to original image coords considering zoom/pan
        img_x = int((x + pan_x) / zoom)
        img_y = int((y + pan_y) / zoom)

        if len(points) < 4:
            points.append((img_x, img_y))
            print(f"Point {len(points)} selected: {img_x, img_y}")

        dragging = True
        last_mouse_pos = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE and dragging:
        # Drag to pan
        dx, dy = x - last_mouse_pos[0], y - last_mouse_pos[1]
        pan_x -= dx
        pan_y -= dy
        last_mouse_pos = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        dragging = False

    elif event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            zoom *= 1.1
        else:
            zoom /= 1.1
        zoom = max(0.2, min(zoom, 10))  # Limit zoom between 0.2x and 10x

cv2.namedWindow("Zoomable Image")
cv2.setMouseCallback("Zoomable Image", mouse_event)

while True:
    # Apply zoom & pan
    transformed = apply_zoom_and_pan(draw_overlay(image))

    cv2.imshow("Zoomable Image", transformed)
    key = cv2.waitKey(30) & 0xFF

    if key == 27:  # ESC to exit
        break
    elif key == ord('r'):  # Reset selection
        points.clear()
        zoom = 1.0
        pan_x, pan_y = 0, 0
        print("Selection reset!")

cv2.destroyAllWindows()
