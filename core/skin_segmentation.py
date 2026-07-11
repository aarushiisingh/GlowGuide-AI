import cv2
import numpy as np

# Face outline
FACE_OVAL = [
    10, 338, 297, 332, 284, 251,
    389, 356, 454, 323, 361, 288,
    397, 365, 379, 378, 400, 377,
    152, 148, 176, 149, 150, 136,
    172, 58, 132, 93, 234, 127,
    162, 21, 54, 103, 67, 109
]

# Left Eye
LEFT_EYE = [
    33, 160, 158, 133,
    153, 144
]

# Right Eye
RIGHT_EYE = [
    362, 385, 387, 263,
    373, 380
]

# Lips
LIPS = [
    61, 146, 91, 181,
    84, 17, 314, 405,
    321, 375, 291, 308
]


def get_points(image, landmarks, indices):

    h, w = image.shape[:2]

    points = []

    for idx in indices:

        lm = landmarks.landmark[idx]

        x = int(lm.x * w)
        y = int(lm.y * h)

        points.append([x, y])

    return np.array(points, dtype=np.int32)


def create_skin_mask(image, landmarks):

    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    face = get_points(image, landmarks, FACE_OVAL)
    left_eye = get_points(image, landmarks, LEFT_EYE)
    right_eye = get_points(image, landmarks, RIGHT_EYE)
    lips = get_points(image, landmarks, LIPS)

    # Fill entire face
    cv2.fillPoly(mask, [face], 255)

    # Remove eyes
    cv2.fillPoly(mask, [left_eye], 0)
    cv2.fillPoly(mask, [right_eye], 0)

    # Remove lips
    cv2.fillPoly(mask, [lips], 0)

    # Extract skin
    skin = cv2.bitwise_and(
        image,
        image,
        mask=mask
    )

    return skin, mask