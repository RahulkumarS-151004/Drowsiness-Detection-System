import cv2
import mediapipe as mp
import math
import pygame
from threading import Thread

# Initialize pygame mixer
pygame.mixer.init()
pygame.mixer.music.load('alarm.mp3')  # Replace with your alarm file path

# Load Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Landmark indices for eyes
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# Function to compute EAR
def eye_aspect_ratio(landmarks, eye_indices):
    p = [landmarks[i] for i in eye_indices]
    vertical_1 = math.dist(p[1], p[5])
    vertical_2 = math.dist(p[2], p[4])
    horizontal = math.dist(p[0], p[3])
    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
    return ear

# Video capture
cap = cv2.VideoCapture(0)
score = 0
threshold = 0.25
frame_limit = 15
alarm_on = False

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        mesh_points = results.multi_face_landmarks[0].landmark
        h, w = frame.shape[:2]
        landmarks = [(int(p.x * w), int(p.y * h)) for p in mesh_points]

        left_ear = eye_aspect_ratio(landmarks, LEFT_EYE)
        right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE)
        avg_ear = (left_ear + right_ear) / 2.0

        for idx in LEFT_EYE + RIGHT_EYE:
            cv2.circle(frame, landmarks[idx], 2, (0, 255, 0), -1)

        if avg_ear < threshold:
            score += 1
            if score >= frame_limit and not alarm_on:
                pygame.mixer.music.play(-1)  # Loop indefinitely
                alarm_on = True
                cv2.putText(frame, "DROWSY!", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        else:
            score = 0
            if alarm_on:
                pygame.mixer.music.stop()
                alarm_on = False

        cv2.putText(frame, f"EAR: {avg_ear:.2f}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Drowsiness Detection', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
