🧩 Rubik’s Cube Scanner & Solver
Computer Vision + Kociemba Two-Phase Algorithm

This project scans a real Rubik’s Cube using your webcam, detects sticker colors using OpenCV, validates the cube state, converts it into a 54-character cube string, and solves it using the Kociemba algorithm.

🚀 Features
🔍 Webcam-Based Cube Scanning

Live 3×3 grid overlay for each face

Detects sticker colors using HSV thresholds

Manual override option

Processes faces in official order:
U, R, F, D, L, B

🎨 Color Calibration Mode

Improve accuracy by calibrating each cube color manually:

    python capture_faces.py --calibrate

🧪 Cube State Validation

validate_input.py checks:

6 faces present

Each face has 9 stickers

Each color appears exactly 9 times

Center colors unique

Final cube string is 54 chars

🧠 Solves Using the Kociemba Algorithm

solve_cube.py generates a sequence of moves to solve the cube.

Example solution:

    R L U2 R L' B2 U2 R2 F2 L2 D2 L2 F2


Saved automatically to:

    solution.txt

🗂 Project Structure

    📁 RubiksCubeScanner-Solver
     ├── capture_faces.py
     ├── validate_input.py
     ├── solve_cube.py
     ├── cube_state.json
     ├── cube_string.txt
     ├── solution.txt
     └── README.md

🧰 Technologies Used

Python

OpenCV

NumPy

Kociemba Solver

JSON

▶️ How to Run the Project
1. Scan Cube Faces

        python capture_faces.py

3. Solve the Cube

       python solve_cube.py

5. Test Mode

        python capture_faces.py --test

💡 Future Enhancements

Automatic cube rotation detection

Smartphone app version

3D visualization of scanned cube

Scramble generator

👨‍💻 Author

Sarthak Kapadne
AI & DS Student | ML & Development Enthusiast
Email: sarthakkapadne6086@gmail.com
