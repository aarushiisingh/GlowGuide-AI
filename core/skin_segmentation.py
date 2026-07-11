CHEEK_LEFT = [
    117, 118, 119, 100, 126,
    142, 203, 206, 205
]

CHEEK_RIGHT = [
    346, 347, 348, 329, 355,
    371, 423, 426, 425
]

FOREHEAD = [
    10, 67, 69, 104,
    108, 109, 151
]

CHIN = [
    152, 148, 176,
    149, 150
]
import numpy as np

def get_landmark_points(image, landmarks, indices):

    h, w, _ = image.shape

    points = []

    for idx in indices:

        landmark = landmarks.landmark[idx]

        x = int(landmark.x * w)
        y = int(landmark.y * h)

        points.append((x, y))

    return np.array(points)

cv2.polylines(
    image,
    [points],
    True,
    (0,255,0),
    2
)