# Contributing to AI Real-time GYM Coach 🏋️‍♂️

Thank you for considering contributing to the AI Real-time GYM Coach project! We welcome improvements, bug reports, and new exercise detectors.

---

## 🛠️ Code of Conduct

Please adhere to the [Code of Conduct](CODE_OF_CONDUCT.md) in all community interactions.

---

## 🚀 How to Contribute

### 1. Reporting Bugs
- Search existing issues to ensure the bug hasn't been reported.
- Open a new issue using our [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md).
- Include reproduction steps, camera setup, Python version, and OS details.

### 2. Suggesting Features & Exercises
- Propose new features or new exercise detectors (e.g., Deadlifts, Pull-ups, Lateral Raises) using our [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md).

### 3. Pull Request Process
1. **Fork** the repository and create a feature branch (`git checkout -b feature/awesome-detector`).
2. **Follow Code Standards**:
   - Subclass `BaseExercise` in `core/base_exercise.py`.
   - Implement `.process(landmarks)` and `.reset()`.
   - Add exercise constants to `services/config/workout_config.py`.
   - Update `requirements.txt` if introducing new libraries.
3. **Test Locally**:
   - Verify webcam input via WebRTC streamer.
   - Test LLM voice coaching feedback triggers.
4. **Commit & Push**:
   - Write clear, descriptive commit messages following Conventional Commits (`feat: ...`, `fix: ...`).
5. **Open a PR**:
   - Fill out the [Pull Request Template](.github/pull_request_template.md).

---

## 🧑‍💻 Development Setup

```bash
# Clone repository
git clone https://github.com/thakurlucky9760-gif/ai-gym-coach.git
cd ai-gym-coach

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run main.py
```
