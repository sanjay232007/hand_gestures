# Hand Gesture-Based Cursor Control System

A Python-based computer vision project that aims to control a computer's mouse cursor using real-time hand gestures captured through a webcam. The project uses hand landmark detection to translate finger movements into mouse actions, reducing the need for a physical mouse.

> **Project status:** In development. The webcam capture test is working. MediaPipe hand tracking is being integrated, and cursor movement, clicking, and scrolling are planned features.

## Table of Contents

- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Planned Features](#planned-features)
- [Technologies Used](#technologies-used)
- [System Architecture](#system-architecture)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation and Setup](#installation-and-setup)
- [Running the Project](#running-the-project)
- [Planned Gesture Mapping](#planned-gesture-mapping)
- [Important Concepts](#important-concepts)
- [Troubleshooting](#troubleshooting)
- [Limitations](#limitations)
- [Privacy and Security](#privacy-and-security)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

Traditional computer interaction relies on physical input devices such as a mouse and keyboard. This project explores an alternative approach using computer vision and hand gesture recognition.

The webcam captures the user's hand, a hand-tracking model identifies important points on the hand, and gesture-processing logic interprets those points to perform mouse actions.

The intended result is a desktop application that allows users to move the cursor, click, and scroll using natural hand movements.

## Objectives

- Implement real-time hand detection using a webcam.
- Understand and use hand landmarks for gesture recognition.
- Map finger coordinates to computer screen coordinates.
- Control the mouse cursor programmatically.
- Implement gesture-based clicking and scrolling.
- Explore computer vision, coordinate transformations, and human-computer interaction.
- Build a modular Python project suitable for learning and portfolio development.

## Planned Features

| Feature | Description | Status |
|---|---|---|
| Webcam capture | Capture live video using OpenCV | Working |
| Hand detection | Detect a hand using MediaPipe | In development |
| Landmark tracking | Identify fingertips and finger joints | Pending |
| Cursor movement | Move the system cursor using the index fingertip | Planned |
| Left and right click | Trigger mouse clicks using gestures | Planned |
| Scrolling | Scroll pages using a designated gesture | Planned |
| Cursor smoothing | Reduce unwanted cursor movement | Planned |
| Error handling | Handle webcam and tracking failures | In development |

## Technologies Used

### Programming language

**Python**

Python is the primary programming language used to develop the application. It provides access to computer vision, machine learning, image processing, and desktop automation libraries.

### Libraries and their responsibilities

| Library | Purpose |
|---|---|
| OpenCV (`opencv-python`) | Access the webcam, capture video frames, process images, draw landmarks, and display the live video feed. |
| MediaPipe (`mediapipe`) | Detect hands and estimate the positions of hand landmarks. The project must use an API compatible with the installed MediaPipe version. |
| PyAutoGUI (`pyautogui`) | Control the system mouse by moving the cursor, clicking, and scrolling. |
| NumPy (`numpy`) | Support numerical operations and coordinate calculations when needed. |

### Development tools

- **Visual Studio Code:** Code editing and project development.
- **Python virtual environment (`venv`):** Isolate project dependencies.
- **Git:** Track source-code changes and versions.
- **GitHub:** Host the source code and document the project.

## System Architecture

The planned application follows this processing pipeline:

1. **Video acquisition:** OpenCV captures frames from the webcam.
2. **Image preparation:** The frame is prepared in the format required by the hand-tracking model.
3. **Hand landmark detection:** MediaPipe identifies the hand and estimates its landmark coordinates.
4. **Gesture recognition:** The application evaluates fingertip positions and distances to determine the intended action.
5. **Coordinate transformation:** Hand coordinates are mapped to screen coordinates.
6. **Mouse control:** PyAutoGUI performs the corresponding mouse action.
7. **Continuous processing:** The pipeline repeats for subsequent frames.

```text
Webcam
   |
   v
OpenCV - Capture and prepare frames
   |
   v
MediaPipe - Detect hand landmarks
   |
   v
Gesture Recognition
   |
   +----> Cursor Movement
   |
   +----> Mouse Click
   |
   +----> Scrolling
   |
   v
PyAutoGUI - Desktop Mouse Control
```

## How It Works

### 1. Webcam capture

OpenCV opens the default webcam and continuously reads video frames.

The webcam frame is represented as an image containing pixel data.

### 2. Hand landmark detection

MediaPipe's hand landmark model can estimate 21 points on a detected hand.

Important landmark indices include:

| Landmark ID | Hand position | Intended use |
|---:|---|---|
| 0 | Wrist | Reference point |
| 4 | Thumb tip | Click gesture |
| 8 | Index fingertip | Cursor movement |
| 12 | Middle fingertip | Gesture recognition |
| 16 | Ring fingertip | Additional gesture recognition |
| 20 | Little finger tip | Additional gesture recognition |

The landmark indices follow MediaPipe's hand landmark convention.

### 3. Coordinate mapping

Landmark coordinates are generally normalized relative to the image dimensions.

For an image with width `W` and height `H`:

```python
pixel_x = int(landmark.x * W)
pixel_y = int(landmark.y * H)
```

These values locate the fingertip in the webcam image. The application will then map the relevant coordinates to the computer screen dimensions.

### 4. Gesture recognition

The application will evaluate fingertip positions, distances, and finger configurations to identify gestures.

For example, the distance between the thumb tip and index fingertip can be used to recognize a pinch gesture.

### 5. Mouse control

Once a gesture is recognized, PyAutoGUI will execute the corresponding system mouse operation.

Movement and clicking must be carefully separated to prevent accidental clicks while moving the cursor.

## Project Structure

The intended project structure is:

```text
hand-gesture-cursor/
│
├── .venv/
│
├── src/
│   ├── main.py
│   ├── hand_tracker.py
│   ├── gestures.py
│   └── cursor_controller.py
│
├── webcam_test.py
├── requirements.txt
├── .gitignore
└── README.md
```

### File descriptions

- `webcam_test.py` — Tests webcam access and displays live video.
- `src/main.py` — Main application entry point that coordinates the modules.
- `src/hand_tracker.py` — Handles hand detection and landmark extraction.
- `src/gestures.py` — Contains gesture recognition logic for clicking and scrolling.
- `src/cursor_controller.py` — Handles cursor movement and mouse actions.
- `requirements.txt` — Lists the project's Python dependencies.
- `.gitignore` — Excludes virtual environments, cache files, and other unnecessary files from Git.
- `README.md` — Documents the project and its setup.

This is the target structure. Files that have not yet been implemented should be added as development progresses.

## Requirements

- Windows 10 or Windows 11.
- A compatible Python installation.
- A working webcam.
- Visual Studio Code or another Python editor.
- An internet connection for installing dependencies.
- A MediaPipe version compatible with the Python version and API used by the project.

The current development environment uses Windows PowerShell and a Python virtual environment.

## Installation and Setup

### Step 1: Clone the repository

If the project is hosted on GitHub:

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd hand-gesture-cursor
```

Replace the placeholder with the actual repository URL.

Alternatively, open the existing project directory in VS Code.

### Step 2: Create a virtual environment

```powershell
py -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install the dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install opencv-python mediapipe pyautogui numpy
```

If installation fails, verify the Python and MediaPipe version compatibility before changing packages.

### Step 4: Record the dependencies

After confirming that the packages are installed, generate `requirements.txt`:

```powershell
python -m pip freeze > requirements.txt
```

This records the installed package versions, including transitive dependencies. For a reproducible project, review the generated file and keep the Python environment consistent.

### Step 5: Verify the imports

```powershell
python -c "import cv2, mediapipe, pyautogui, numpy; print('All imports successful')"
```

If successful, the terminal should display:

```text
All imports successful
```

## Running the Project

### Test the webcam

Run:

```powershell
python webcam_test.py
```

A window should display the live webcam feed. Press `q` while the window is focused to close it.

### Run the hand tracker

Once the hand-tracking implementation is compatible with the installed MediaPipe version:

```powershell
python src/hand_tracker.py
```

The intended result is a live video feed with the detected hand landmarks and an index-fingertip marker.

### Run the complete application

The complete application will be launched using:

```powershell
python src/main.py
```

This command will become usable once the main application and its supporting modules have been implemented.

## Planned Gesture Mapping

The following gestures are proposed for the application and are not yet confirmed as implemented.

| Gesture | Intended action |
|---|---|
| Move the index fingertip | Move the mouse cursor |
| Bring thumb and index fingertip together | Left click |
| Use a separate, defined gesture | Right click |
| Raise the index and middle fingers in a defined configuration | Scroll |
| Hold a recognized gesture | Potentially enable a drag operation in a future version |

The final gesture definitions may change during development to improve reliability and prevent accidental actions.

## Important Concepts

### Computer vision

Computer vision enables a computer to extract useful information from images and video. This project uses it to identify hand positions in webcam frames.

### Hand landmarks

Landmarks are estimated points that describe the structure and position of the hand. Their coordinates are used as inputs to the gesture recognition system.

### Coordinate transformation

The webcam and computer screen may have different dimensions. Coordinate transformation maps a fingertip's position in the camera image to the corresponding position on the screen.

### Gesture recognition

Gesture recognition interprets hand positions or movements as commands. The application can use fingertip distances, finger states, and thresholds to identify actions.

### Cursor smoothing

Small variations in detected landmark positions can make the cursor jitter. Smoothing methods, such as exponential moving averages, can reduce unwanted movement.

### Real-time processing

The application must process frames quickly enough to provide responsive cursor control. Model inference time, webcam frame rate, and gesture processing all affect responsiveness.

## Troubleshooting

### 1. `AttributeError: module 'mediapipe' has no attribute 'solutions'`

**Cause:** The installed MediaPipe package does not expose the legacy `mp.solutions` API used in the initial example, or Python is importing an unexpected module.

Check the installed version and module location:

```powershell
python -c "import mediapipe as mp; print(mp.__version__); print(mp.__file__); print(hasattr(mp, 'solutions'))"
```

The implementation should be adapted to the API available in the installed version. The newer task-based `mp.tasks.vision.HandLandmarker` API is an alternative, but it requires a compatible model file and a different implementation.

Do not assume that reinstalling the latest version will make legacy code work.

### 2. Webcam cannot be opened

Check that:

- The webcam is connected or enabled.
- Windows camera permissions allow desktop applications to access it.
- Another application is not exclusively using the camera.
- The correct camera index is selected in OpenCV.

### 3. Hand landmarks are not detected

Check that:

- The hand is clearly visible.
- Lighting is sufficient.
- The hand is within the camera frame.
- The model and its required assets are available.
- The input image uses the expected color format.

### 4. Cursor movement is jittery

Potential improvements include smoothing the fingertip coordinates, restricting movement to a calibrated region, and filtering small movements.

### 5. Mouse clicks trigger accidentally

Use a distance threshold, gesture-state tracking, and a short cooldown between clicks. The application should also require a clear transition into a click gesture instead of triggering a click on every frame.

## Limitations

- Performance depends on webcam quality, lighting, and hand visibility.
- Landmark detection can become unreliable when fingers overlap or leave the frame.
- Coordinate mapping may require calibration for different screen sizes.
- Gesture thresholds may need adjustment for different users.
- Cursor smoothing can introduce a small amount of latency.
- System-level mouse control may behave differently across applications and operating systems.
- The project's hand tracking and mouse-control features remain under development.

## Privacy and Security

The intended design processes webcam frames locally on the computer.

- Camera access is required while the application is running.
- Webcam frames should not be uploaded or stored unless a future feature explicitly requires it.
- Mouse-control operations should only run when the user has started the application.
- The application should provide a reliable way to stop tracking and release any pressed mouse buttons.
- Users should close the application when they no longer want camera-based tracking.

## Future Improvements

Potential improvements include:

- More reliable hand tracking and gesture recognition.
- Smooth cursor movement using filtering algorithms.
- Adjustable cursor sensitivity and calibration.
- Right-click and drag-and-drop support.
- Scroll-speed configuration.
- A graphical interface with start, stop, and status controls.
- Gesture customization.
- Performance measurement, including frame rate and tracking latency.
- Cross-platform support.
- Automated tests for gesture recognition and coordinate mapping.

## Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Commit your changes with a descriptive message.
5. Open a pull request explaining the changes.

Please ensure that changes do not introduce unintended mouse clicks or leave mouse buttons pressed when tracking stops.

## License

No license has been selected yet. Choose an appropriate open-source license before distributing the project. For example, the MIT License permits reuse under its stated conditions.

If you choose MIT, add a `LICENSE` file containing the appropriate license text and copyright notice.

## Author

**Author:** [Your Name]

**GitHub:** [Your GitHub Profile URL]

## Acknowledgements

This project builds on the Python computer vision ecosystem, including OpenCV, MediaPipe, PyAutoGUI, and NumPy.

Their documentation is useful for understanding the libraries and extending the application:

- OpenCV: https://docs.opencv.org/
- MediaPipe: https://ai.google.dev/edge/mediapipe/solutions/guide
- PyAutoGUI: https://pyautogui.readthedocs.io/
- NumPy: https://numpy.org/doc/

---

*This README describes the intended design and current development status. Update the feature-status table and usage instructions as each component becomes functional.*
