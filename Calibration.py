import cv2
import numpy as np

image_path = 'ruler.jpg'  # Change to your image
image = cv2.imread(image_path)
if image is None:
    raise ValueError("Image not found!")

clone = image.copy()
points = []
pixel_per_mm = None
ref_length_mm = 1.0 # <-- Set known reference length in mm

def click_event(event, x, y, flags, param):
    global points, clone, pixel_per_mm
    
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        
        if len(points) % 2 == 1:
            # First point of the pair
            cv2.circle(clone, (x, y), 1, (0, 0, 255), -1)
        else:
            # Second point: force horizontal line
            x1, y1 = points[-2]
            x2, y2 = x, y
            
            # Force horizontal line using first point's y
            y2 = y1
            
            # Update last point to horizontal
            points[-1] = (x2, y2)
            
            # Draw line and points
            cv2.circle(clone, (x2, y2), 1, (0, 0, 255), -1)
            cv2.line(clone, (x1, y1), (x2, y2), (0, 255, 0), 1)

            # Calculate horizontal distance
            distance_px = abs(x2 - x1)
            print(f"Horizontal distance: {distance_px:.2f} px")

            if pixel_per_mm is None:
                # First measurement is reference
                pixel_per_mm = distance_px / ref_length_mm
                print(f"Pixel per mm ratio: {pixel_per_mm:.2f} px/mm")
                cv2.putText(clone, f"Ref: {ref_length_mm}mm", (x2, y2-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 1)
            else:
                # Measure new object
                real_size_mm = distance_px / pixel_per_mm
                print(f"Measured object size: {real_size_mm:.2f} mm")
                cv2.putText(clone, f"{real_size_mm:.2f} mm", (x2, y2-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 1)

        cv2.imshow("Image", clone)

cv2.imshow("Image", clone)
cv2.setMouseCallback("Image", click_event)

print("Click 2 points for horizontal measurement: first reference, then objects...")
cv2.waitKey(0)
cv2.destroyAllWindows()
