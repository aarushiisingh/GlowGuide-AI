import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

FACE_MESH = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
)

def detect_face_mesh(image):

    image = np.array(image)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = FACE_MESH.process(rgb_image)

    landmarks = None

    if results.multi_face_landmarks:

        landmarks = results.multi_face_landmarks[0]

        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION
        )

    return {
        "image": image,
        "landmarks": landmarks
    }