# AI Fitness Coach

Real-time exercise tracking with pose estimation. Counts reps and gives live form feedback — no gym equipment or wearables needed.

<!-- Replace with your actual demo GIF -->
![Demo](demo.gif)

## Features

- **3 exercises supported:** Squats, Pushups, Bicep Curls
- **Rep counting** via joint angle state machine
- **Form feedback** with color-coded overlay (green = good, red = correction needed)
- **~30 FPS** on CPU (MediaPipe, no GPU required)
- **Two modes:** CLI (OpenCV window) or Web UI (Streamlit)

## How It Works

1. MediaPipe Pose detects 33 body landmarks from the webcam feed
2. Joint angles are computed at key joints (hip-knee-ankle for squats, etc.)
3. A state machine transitions between `up`/`down` states to count reps
4. Angle thresholds trigger form feedback in real time

### Angle Thresholds

| Exercise | Joint | Down | Up | Form Check |
|----------|-------|------|----|------------|
| Squat | Knee | < 90° | > 160° | Knee behind toes |
| Pushup | Elbow | < 90° | > 160° | Body alignment 155–200° |
| Bicep Curl | Elbow | > 160° | < 40° | Minimal shoulder swing |

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/ai-fitness-coach
cd ai-fitness-coach
pip install -r requirements.txt
```

## Usage

### CLI (OpenCV window)
```bash
python main.py --exercise squat
python main.py --exercise pushup
python main.py --exercise curl
```
- Press `q` to quit
- Press `r` to reset rep count

### Web UI (Streamlit)
```bash
streamlit run app.py
```
Then open `http://localhost:8501` and allow webcam access.

## Project Structure

```
ai-fitness-coach/
├── main.py              # CLI entry point
├── app.py               # Streamlit web UI
├── pose_detector.py     # MediaPipe wrapper
├── exercises/
│   ├── base.py          # Abstract Exercise class
│   ├── squat.py
│   ├── pushup.py
│   └── curl.py
├── utils/
│   ├── angles.py        # Joint angle calculation
│   └── drawing.py       # Overlay rendering
└── requirements.txt
```

## Tech Stack

- [MediaPipe](https://mediapipe.dev/) — pose estimation
- [OpenCV](https://opencv.org/) — video capture & drawing
- [Streamlit](https://streamlit.io/) + [streamlit-webrtc](https://github.com/whitphx/streamlit-webrtc) — web UI
- NumPy — angle math
