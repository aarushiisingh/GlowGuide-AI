import cv2
import mediapipe as mp
import numpy as np

from core.skin_segmentation import create_skin_mask

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
)


def detect_face_mesh(image):

    image = np.array(image)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    skin = None
    mask = None
    landmarks = None

    if results.multi_face_landmarks:

        landmarks = results.multi_face_landmarks[0]

        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing.DrawingSpec(
                color=(255, 255, 255),
                thickness=1,
                circle_radius=1
            )
        )

        skin, mask = create_skin_mask(
            image,
            landmarks
        )

    return {
        "image": image,
        "skin": skin,
        "mask": mask,
        "landmarks": landmarks
    }