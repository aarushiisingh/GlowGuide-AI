import cv2
import numpy as np


class ColorAnalyzer:

    def __init__(self):
        pass

    def average_skin_color(self, skin):

        pixels = skin.reshape((-1, 3))

        pixels = pixels[np.any(pixels != [0, 0, 0], axis=1)]

        if len(pixels) == 0:
            return None

        return np.mean(pixels, axis=0)

    def rgb_to_lab(self, rgb):

        rgb = np.uint8([[rgb]])

        lab = cv2.cvtColor(
            rgb,
            cv2.COLOR_BGR2LAB
        )

        return lab[0][0]

    def calculate_ita(self, lab):

        L = float(lab[0])

        b = float(lab[2])

        if b == 0:
            b = 0.01

        ita = np.degrees(
            np.arctan(
                (L - 50) / b
            )
        )

        return ita

    def classify_skin(self, ita):

        if ita > 55:
            return "Very Light"

        elif ita > 41:
            return "Light"

        elif ita > 28:
            return "Neutral"

        elif ita > 10:
            return "Tan"

        elif ita > -30:
            return "Brown"

        return "Deep"

    def detect_undertone(self, lab):

        a = lab[1]

        b = lab[2]

        if b > a + 8:
            return "Warm"

        elif a > b + 8:
            return "Cool"

        return "Neutral"

    def analyze(self, skin):

        rgb = self.average_skin_color(skin)

        if rgb is None:
            return None

        lab = self.rgb_to_lab(rgb)

        ita = self.calculate_ita(lab)

        tone = self.classify_skin(ita)

        undertone = self.detect_undertone(lab)

        return {
            "rgb": rgb.astype(int),
            "lab": lab.astype(int),
            "ita": round(ita, 2),
            "tone": tone,
            "undertone": undertone
        }
    
# Create one analyzer object
_analyzer = ColorAnalyzer()

def analyze_skin(skin):
    """
    Wrapper function for app.py
    """
    return _analyzer.analyze(skin)