# AI Real-time GYM Coach 🏋️‍♂️

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.54.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Pose%20Landmarker-0097A7?style=for-the-badge&logo=google&logoColor=white)](https://developers.google.com/mediapipe)
[![Groq LLM](https://img.shields.io/badge/Groq-Ultra--Fast%20Inference-F55036?style=for-the-badge)](https://groq.com/)
[![WebRTC](https://img.shields.io/badge/WebRTC-Low%20Latency%20Video-333333?style=for-the-badge&logo=webrtc&logoColor=white)](https://github.com/whitphx/streamlit-webrtc)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

An intelligent, real-time computer vision fitness coaching application. Using **MediaPipe Pose Landmarker**, **Streamlit-WebRTC**, **Groq Ultra-Fast LLMs**, and automated **Text-to-Speech (TTS)**, this coach tracks your joint kinematics, counts repetitions, diagnoses postural flaws, and provides spoken voice corrections in real time.

---

## 🌟 Key Highlights

- **⚡ Real-Time Pose Tracking**: 33 full-body 3D landmarks tracked via Google's `pose_landmarker_full.task` running on video stream.
- **📐 Biomechanical Kinematics**: Computes vector-based joint angles (elbow flexion, knee flexion, hip angle, torso inclination) frame-by-frame.
- **🎙️ AI Voice Coaching**: Integrated with Groq LLM (`openai/gpt-oss-120b`, `openai/gpt-oss-20b`, `qwen/qwen3.8-27b`) generating concise 10–15 word professional coaching cues delivered through `gTTS` audio autoplay.
- **📊 Form Validation & Rep Counting**: Multi-phase state machine ensuring full range of motion (ROM) before incrementing rep counts.
- **💾 Local SQLite Session Persistence**: Tracks total workouts, completed sets, reps, and form anomalies in a lightweight local database.
- **🎨 Dark Futuristic HUD Interface**: Custom styled UI with real-time biometric metrics, video feed overlay, and session controls.

---

## 🏋️‍♂️ Supported Exercises & Kinematic Metrics

| Exercise | Primary Joint Angle | Biomechanical Checks | Form Error Detections |
| :--- | :--- | :--- | :--- |
| **Squats** | Knee Angle (Hip-Knee-Ankle) | Hip/Back Angle, Depth Ratio | Incomplete depth, knee collapse, excessive forward torso lean |
| **Push-ups** | Elbow Angle (Shoulder-Elbow-Wrist) | Body Linear Alignment, Hip Level | Flared elbows, hip sag, hip pike, incomplete lockout |
| **Biceps Curls** | Elbow Flexion/Extension | Shoulder Stability, Torso Sway | Torso swinging, elbow drifting forward, incomplete contraction |
| **Shoulder Press** | Elbow Overhead Extension | Back Arch, Bilateral Symmetry | Excessive lumbar arching, asymmetrical press, partial lockout |
| **Lunges** | Front Knee Angle | Torso Verticality, Stride Balance | Front knee overextension past toes, excessive forward tilt, loss of balance |

---

## 🏗️ System Architecture

```
[ User Webcam ]
       │
       ▼ (WebRTC Video Stream)
[ OpenCV & MediaPipe Pose Landmarker ]
       │  Extracts 33 Landmarks (x, y, z)
       ▼
[ Kinematics & Detector Engine ]
   ├── Angle Calculations (Knee, Elbow, Hip, Torso)
   ├── State Machine (Rep Completion, Range of Motion)
   └── Form Fault Detection (Sag, Sway, Depth, Arch)
       │
       ├───► [ HUD Metrics & Skeleton Visualizer ] ──► [ Streamlit UI ]
       │
       ▼ (Event: Error Detected / Rep / Set Completed)
[ Groq LLM Coaching Engine ]
   ├── High-speed context inference (gpt-oss-120b / qwen3.8-27b)
   └── Generates natural, sharp 10-15 word audio cue
       │
       ▼
[ gTTS Voice Synthesizer & Autoplay ] ──► [ Audio Output ]
       │
       ▼
[ SQLite Database (data.db) ] ──► Session Analytics & History
```

---

## 📁 Project Structure

```
ai-gym-coach/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── workflows/
│   │   └── ci.yml
│   └── pull_request_template.md
├── .streamlit/
│   ├── config.toml                 # Streamlit theme & server options
│   ├── secrets.toml.example        # Example secrets configuration
│   └── secrets.toml                # Local Groq API key configuration
├── core/
│   ├── __init__.py
│   └── base_exercise.py            # Base abstract class with angle math
├── detectors/
│   ├── __init__.py
│   ├── bicep_curl.py               # Biceps curls kinematic detector
│   ├── lunges.py                   # Lunges kinematic detector
│   ├── pushup.py                   # Push-ups alignment & rep detector
│   ├── shoulder_press.py           # Overhead press detector
│   └── squat.py                    # Squat depth & back angle detector
├── ml_models/
│   ├── __init__.py
│   └── pose_landmarker_full.task   # MediaPipe full-body pose model
├── pages/
│   └── __init__.py
├── services/
│   ├── auth/
│   │   └── login_wall.py           # User profile & session initialization
│   ├── coaching/
│   │   ├── llm.py                  # Groq API client with model fallback
│   │   ├── tts.py                  # gTTS audio generation
│   │   └── voice_pipeline.py       # Event orchestration & autoplay
│   ├── config/
│   │   └── workout_config.py       # Exercise list, metrics & coach prompts
│   ├── persistence/
│   │   └── exercise_repository.py  # SQLite database schema & queries
│   ├── state/
│   │   └── session_defaults.py     # Streamlit session state initialization
│   ├── tracking/
│   │   └── metrics.py              # Real-time state synchronizer
│   ├── ui/
│   │   └── style_loader.py         # CSS and custom font injection
│   └── vision/
│       ├── __init__.py
│       └── exercise_video_processor.py # WebRTC video frame processor
├── static/
│   ├── AdobeClean.otf              # Local UI typography
│   └── style.css                   # Futuristic dark UI stylesheet
├── tutorial-info/                  # Reference tutorials & version history
├── .env.example                    # Environment variable template
├── .gitattributes                  # LF normalization & binary asset tags
├── .gitignore                      # Python, Streamlit, DB, and OS ignore rules
├── CODE_OF_CONDUCT.md              # Contributor Covenant v2.1
├── CONTRIBUTING.md                 # Contribution guidelines
├── LICENSE                         # MIT License
├── packages.txt                    # Linux system dependencies (for cloud deploy)
├── requirements.txt                # Python dependencies
├── run.bat                         # Windows one-click batch launcher
├── run.ps1                         # Windows PowerShell launcher
└── main.py                         # Streamlit application entry point
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python**: 3.10 or 3.11 recommended.
- **Webcam**: Standard USB or built-in webcam.
- **Groq API Key**: Free API key from [Groq Console](https://console.groq.com/keys).

### 2. Clone the Repository
```bash
git clone https://github.com/thakurlucky9760-gif/ai-gym-coach.git
cd ai-gym-coach
```

### 3. Create & Activate Virtual Environment
On Windows:
```powershell
python -m venv venv
.\venv\Scripts\activate
```

On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **Note for Linux Users**: Install OpenCV and WebRTC system dependencies:
> ```bash
> sudo apt-get update && sudo apt-get install -y libgl1 libglib2.0-0 libsm6 libxext6
> ```

### 5. Configure API Key
Create a `.env` file in the project root (or copy from `.env.example`):
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```

Or configure via `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "gsk_your_groq_api_key_here"
```

### 6. Run the Application

#### Option A: One-Click Launcher (Windows)
Double-click `run.bat` or run in PowerShell:
```powershell
.\run.ps1
```

#### Option B: Standard Streamlit Command
```bash
streamlit run main.py
```

The application will open in your browser at **http://localhost:8501**.

---

## 🎙️ Groq LLM Coaching Pipeline

The coach dynamically selects from ultra-fast inference models on Groq:
1. `openai/gpt-oss-120b` (Primary high-accuracy conversational reasoning)
2. `openai/gpt-oss-20b` (Ultra-low latency fallback)
3. `qwen/qwen3.8-27b` (High-efficiency alternative)
4. `llama-3.3-70b-versatile` (Robust versatile backup)

If no internet or API limit is reached, a graceful heuristic coaching cue is provided offline so workouts are never interrupted.

---

## ☁️ Deployment Guide

### Streamlit Community Cloud
1. Push this repository to your GitHub account.
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a new app.
3. Select this repository and branch `main`.
4. Set main file path to `main.py`.
5. Under **Advanced Settings** -> **Secrets**, add:
   ```toml
   GROQ_API_KEY = "gsk_your_groq_api_key_here"
   ```
6. Click **Deploy**! `packages.txt` will automatically install necessary Linux system libraries.

---

## 🤝 Contributing

Contributions are welcome! Please check out [CONTRIBUTING.md](CONTRIBUTING.md) for full instructions on creating issues, proposing new exercises, and opening pull requests.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) - Copyright (c) 2026 Chaitanya Pratap.
