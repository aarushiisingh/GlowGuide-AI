import math


class FaceShapeAnalyzer:

    def distance(self, p1, p2):
        return math.sqrt(
            (p1[0] - p2[0])**2 +
            (p1[1] - p2[1])**2
        )

    def landmark_to_pixel(self, landmark, width, height):

        return (
            int(landmark.x * width),
            int(landmark.y * height)
        )

    def analyze(self, image, landmarks):

        h, w = image.shape[:2]

        lm = landmarks.landmark

        # -----------------------------
        # Important landmarks
        # -----------------------------

        forehead_left = self.landmark_to_pixel(lm[54], w, h)
        forehead_right = self.landmark_to_pixel(lm[284], w, h)

        cheek_left = self.landmark_to_pixel(lm[234], w, h)
        cheek_right = self.landmark_to_pixel(lm[454], w, h)

        jaw_left = self.landmark_to_pixel(lm[172], w, h)
        jaw_right = self.landmark_to_pixel(lm[397], w, h)

        chin = self.landmark_to_pixel(lm[152], w, h)
        forehead = self.landmark_to_pixel(lm[10], w, h)

        forehead_width = self.distance(
            forehead_left,
            forehead_right
        )

        cheek_width = self.distance(
            cheek_left,
            cheek_right
        )

        jaw_width = self.distance(
            jaw_left,
            jaw_right
        )

        face_height = self.distance(
            forehead,
            chin
        )

        ratio = face_height / cheek_width

        # -----------------------------
        # Classification
        # -----------------------------

        if ratio > 1.5:

            shape = "Oblong"

        elif (
            forehead_width > jaw_width and
            jaw_width < cheek_width * 0.85
        ):

            shape = "Heart"

        elif abs(forehead_width - jaw_width) < 20:

            shape = "Square"

        elif abs(face_height - cheek_width) < 30:

            shape = "Round"

        else:

            shape = "Oval"

        return {

            "shape": shape,

            "measurements": {

                "forehead": round(forehead_width, 1),
                "cheek": round(cheek_width, 1),
                "jaw": round(jaw_width, 1),
                "height": round(face_height, 1),
                "ratio": round(ratio, 2)

            }

        }


analyzer = FaceShapeAnalyzer()


def analyze_face_shape(image, landmarks):

    return analyzer.analyze(
        image,
        landmarks
    )