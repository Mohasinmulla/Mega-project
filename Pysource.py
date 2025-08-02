import cv2

points = []  # store up to 4 points

def select_border(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((x, y))
            print(f"Point {len(points)} selected: {x, y}")

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", select_border)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if len(points) == 4:
        # Extract vertical and horizontal line positions
        x1, _ = points[0]  # Left vertical
        x2, _ = points[1]  # Right vertical
        _, y1 = points[2]  # Top horizontal
        _, y2 = points[3]  # Bottom horizontal

        # Draw 2 vertical lines
        cv2.line(frame, (x1, 0), (x1, frame.shape[0]), (0, 255, 0), 2)
        cv2.line(frame, (x2, 0), (x2, frame.shape[0]), (0, 255, 0), 2)

        # Draw 2 horizontal lines
        cv2.line(frame, (0, y1), (frame.shape[1], y1), (0, 255, 0), 2)
        cv2.line(frame, (0, y2), (frame.shape[1], y2), (0, 255, 0), 2)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC to exit
        break
    elif key == ord('r'):  # Press 'r' to reset selection
        points = []
        print("Selection reset!")

cap.release()
cv2.destroyAllWindows()
