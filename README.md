# ALPA — AI Translation App

> **Repository:** [alpamidha-prog/Translation_App](https://github.com/alpamidha-prog/Translation_App)
> **Topic:** Supervised Learning

---

## Overview

**ALPA** is a real-time voice translation desktop application that translates speech between **English and Finnish**. It features a modern dark-themed GUI built with `customtkinter`, live speech recognition via Google's API, and an optional camera preview window.

---

## Screenshots

<p align="center">
  <img src="screenshot1.png" alt="Finnish to English Translation" width="400">
  <br>
  <em>Finnish to English Translation</em>
</p>

<p align="center">
  <img src="screenshot2.png" alt="English to Finnish Translation" width="400">
  <br>
  <em>English to Finnish Translation</em>
</p>

---

## Features

- **Bidirectional voice translation** — English ↔ Finnish, switchable via a toggle
- **Live speech recognition** — captures and transcribes spoken input in real time
- **Instant translation** — uses `deep_translator` (GoogleTranslator) to translate recognized text
- **Camera preview** — opens a live webcam feed in a separate window
- **Clean dark UI** — built with `customtkinter` in a dark mode with a vibrant red-pink accent theme

---

## Tech Stack

| Layer | Technology |
|---|---|
| GUI | `customtkinter` (CustomTkinter) |
| Speech Recognition | `SpeechRecognition` + Google Speech API |
| Translation | `deep_translator` (GoogleTranslator) |
| Camera | `OpenCV` (`cv2`) |
| Image Handling | `Pillow` (PIL) |
| Concurrency | `threading` (Python standard library) |

---

## Project Structure

```
Translation_App/
├── translator.py   # Main application — GUI, speech recognition & translation logic
├── index.html      # Web front-end entry point
├── script.js       # Front-end JavaScript logic
└── styles.css      # Front-end styling
```

**Language breakdown:**
- Python — 33.3%
- CSS — 28.9%
- JavaScript — 26.6%
- HTML — 11.2%

---

## How It Works

1. The user selects a translation direction (EN → FI or FI → EN) using the toggle switch.
2. Clicking **Start Listening** opens the microphone and begins ambient noise calibration.
3. Spoken audio is captured and sent to Google's Speech Recognition API for transcription.
4. The transcribed text is translated using `GoogleTranslator` and displayed in the text box in the format:

   ```
   [EN] Hello, how are you?
   [FI] Hei, miten voit?
   ```

5. The session can be stopped at any time with **Stop Listening**, and the text box cleared with **Clear**.
6. **Open Camera** launches a live OpenCV webcam preview in a separate window (press `q` to close it).

---

## Getting Started

### Prerequisites

Install the required Python packages:

```bash
pip install customtkinter SpeechRecognition deep-translator opencv-python Pillow
```

### Run the App

```bash
python translator.py
```

---

## Notes

- An active internet connection is required for both speech recognition (Google Speech API) and translation (GoogleTranslator).
- Microphone access must be permitted by the operating system.
- The camera feature is optional and uses the default system webcam (device index `0`).

---

## Author

**alpamidha-prog** — [GitHub Profile](https://github.com/alpamidha-prog)
