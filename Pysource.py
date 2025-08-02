import cv2

points = []

def draw_circle(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:  # Left mouse click
        points.append((x, y))

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", draw_circle)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Draw points
    for pt in points:
        cv2.circle(frame, pt, radius=2, color=(25, 15, 255), thickness=-1)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF  # Use correct function
    if key == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
