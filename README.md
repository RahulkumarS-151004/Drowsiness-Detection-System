# Drowsiness-Detection-System

A real-time drowsiness detection system built with Python, OpenCV, and MediaPipe, designed to monitor a person’s eyes and trigger an alarm if drowsiness is detected. Ideal for applications like driver monitoring, fatigue detection, and safety systems.

**🚀 Features**

⏱️ Real-time video stream processing

👁️ Eye Aspect Ratio (EAR) based eye closure detection

🔊 Alarm system via Pygame to alert on drowsiness

🧠 Facial landmark tracking with MediaPipe Face Mesh

✅ Lightweight and works with regular webcams


**📸 How It Works**

Captures video using OpenCV.

Detects facial landmarks with MediaPipe's Face Mesh.

Calculates EAR (Eye Aspect Ratio) for both eyes.

If eyes remain closed (EAR below threshold) for a set number of frames:

Plays an alarm sound using Pygame.

Displays real-time EAR and status on-screen.


**🧠 Technologies Used**

Python

OpenCV

MediaPipe

Pygame

Math / Threading / Collections
