import cv2
import numpy as np
import json
from validate_input import validate_cube_state

# Define HSV color ranges for basic cube colors (can be calibrated)
color_ranges = {
    'W': ([0, 0, 200], [180, 30, 255]),      # white
    'R': ([0, 100, 100], [10, 255, 255]),     # red
    'O': ([10, 100, 100], [25, 255, 255]),    # orange
    'Y': ([25, 100, 100], [35, 255, 255]),    # yellow
    'G': ([35, 100, 100], [85, 255, 255]),    # green
    'B': ([85, 100, 100], [125, 255, 255])    # blue
}

# Standard face order (U, R, F, D, L, B)
face_order = ['U', 'R', 'F', 'D', 'L', 'B']
scanned_faces = {}
face_index = 0
test_mode = False

def calibrate_colors():
    """Optional calibration function to improve color detection"""
    print("\n🎨 Color Calibration Mode")
    print("Show each color to the camera and press the corresponding key:")
    print("W - White, R - Red, O - Orange, Y - Yellow, G - Green, B - Blue")
    
    cap = cv2.VideoCapture(0)
    calibrated_colors = {}
    
    for color, key in zip(['W', 'R', 'O', 'Y', 'G', 'B'], [ord('w'), ord('r'), ord('o'), ord('y'), ord('g'), ord('b')]):
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
                
            frame = cv2.flip(frame, 1)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            roi = hsv[200:240, 280:320]  # Center region
            
            cv2.rectangle(frame, (280, 200), (320, 240), (0, 255, 0), 2)
            cv2.putText(frame, f"Calibrate {color}", (30, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(frame, "Press the color key when ready", (30, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.imshow("Calibration", frame)
            
            k = cv2.waitKey(1) & 0xFF
            if k == 27:  # ESC to exit
                cap.release()
                cv2.destroyAllWindows()
                return color_ranges
            elif k == key:
                avg_hsv = np.mean(roi.reshape(-1, 3), axis=0)
                # Create range around the detected color
                lower = [max(0, avg_hsv[0] - 10), max(0, avg_hsv[1] - 50), max(0, avg_hsv[2] - 50)]
                upper = [min(180, avg_hsv[0] + 10), min(255, avg_hsv[1] + 50), min(255, avg_hsv[2] + 50)]
                color_ranges[color] = (lower, upper)
                print(f"Calibrated {color}: {lower} - {upper}")
                break
    
    cap.release()
    cv2.destroyAllWindows()
    return color_ranges

def classify_color(hsv_pixel):
    for key, (lower, upper) in color_ranges.items():
        lower_np = np.array(lower)
        upper_np = np.array(upper)
        if cv2.inRange(np.uint8([[hsv_pixel]]), lower_np, upper_np):
            return key
    return '?'

def draw_grid(frame, detected=None):
    h, w, _ = frame.shape
    offset_x = w//2 - 75
    offset_y = h//2 - 75
    size = 50

    for i in range(3):
        for j in range(3):
            x = offset_x + j * size
            y = offset_y + i * size
            color = (0, 255, 0)
            thickness = 2
            if detected and i == 1 and j == 1:  # Highlight center
                thickness = 4
            cv2.rectangle(frame, (x, y), (x + size, y + size), color, thickness)
            if detected:
                cv2.putText(frame, detected[i * 3 + j], (x + 12, y + 35), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

def detect_colors(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, w, _ = frame.shape
    offset_x = w//2 - 75
    offset_y = h//2 - 75
    size = 50

    detected = []
    for i in range(3):
        for j in range(3):
            x = offset_x + j * size + 15
            y = offset_y + i * size + 15
            roi = hsv[y:y+20, x:x+20]
            avg = np.mean(roi.reshape(-1, 3), axis=0)
            detected.append(classify_color(avg))
    return detected

def save_cube_state():
    """Save the cube state to JSON and generate the cube string"""
    with open('cube_state.json', 'w') as f:
        json.dump(scanned_faces, f)
    
    # Process the cube state to string format
    center_mapping = {}
    for face in face_order:
        center_color = scanned_faces[face][4]
        center_mapping[center_color] = face

    cube_string = ''
    for face in face_order:
        for color in scanned_faces[face]:
            cube_string += center_mapping[color]
    
    with open('cube_string.txt', 'w') as f:
        f.write(cube_string)
    
    return cube_string

def load_test_cube():
    """Load a predefined test cube state for development"""
    test_cube = {
        "U": ["W", "W", "W", "W", "W", "W", "W", "W", "W"],
        "R": ["R", "R", "R", "R", "R", "R", "R", "R", "R"],
        "F": ["G", "G", "G", "G", "G", "G", "G", "G", "G"],
        "D": ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],
        "L": ["O", "O", "O", "O", "O", "O", "O", "O", "O"],
        "B": ["B", "B", "B", "B", "B", "B", "B", "B", "B"]
    }
    return test_cube

def main():
    global face_index, scanned_faces, test_mode
    
    # Check for test mode argument
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_mode = True
        scanned_faces = load_test_cube()
        cube_string = save_cube_state()
        print("\n🧪 Test cube loaded successfully!")
        print(f"Generated cube string: {cube_string}")
        if validate_cube_state(scanned_faces):
            print("✅ Cube state is valid")
        else:
            print("❌ Cube state is invalid")
        return
    
    # Check for calibration argument
    if len(sys.argv) > 1 and sys.argv[1] == "--calibrate":
        global color_ranges
        color_ranges = calibrate_colors()
        print("\nCalibration complete. New color ranges:")
        for color, (lower, upper) in color_ranges.items():
            print(f"{color}: {lower} - {upper}")
        return

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    current_detected = []
    confirmed = False

    while face_index < len(face_order):
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame")
            break

        frame = cv2.flip(frame, 1)
        draw_grid(frame, current_detected if confirmed else None)

        # Instruction
        face_name = face_order[face_index]
        cv2.putText(frame, f"Show {face_name} face (center: {face_name})", (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 4)
        cv2.putText(frame, f"Show {face_name} face (center: {face_name})", (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        if confirmed:
            cv2.putText(frame, f"Detected: {' '.join(current_detected)}", (30, 420),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "SPACE: Retake | ENTER: Confirm | M: Manual", (30, 450),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.imshow("Rubik's Cube Scanner", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC to exit
            break

        if key == ord(' ') or (not confirmed and key == 13):
            current_detected = detect_colors(frame)
            confirmed = True

        elif key == 13 and confirmed:  # ENTER to confirm
            scanned_faces[face_name] = current_detected
            face_index += 1
            confirmed = False
            current_detected = []

        elif key == ord('m') and confirmed:  # Manual input
            manual_input = input(f"Enter colors for {face_name} face (9 chars, WROYGB): ").upper()
            if len(manual_input) == 9 and all(c in 'WROYGB' for c in manual_input):
                scanned_faces[face_name] = list(manual_input)
                face_index += 1
                confirmed = False
                current_detected = []
            else:
                print("Invalid input! Must be 9 characters from W, R, O, Y, G, B")

    cap.release()
    cv2.destroyAllWindows()

    if face_index == len(face_order):
        cube_string = save_cube_state()
        print("\n✅ All faces scanned! Cube state:")
        for face, colors in scanned_faces.items():
            print(f"{face}: {' '.join(colors)}")
        
        if validate_cube_state(scanned_faces):
            print(f"\nGenerated cube string: {cube_string}")
            print("\nYou can now run solve_cube.py to get the solution!")
        else:
            print("\n❌ Cube state is invalid. Please rescan.")

if __name__ == "__main__":
    main()