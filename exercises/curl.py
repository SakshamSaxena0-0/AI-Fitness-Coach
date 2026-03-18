from .base import Exercise
from utils.angles import calculate_angle


class Curl(Exercise):
    name = "curl"

    def __init__(self):
        super().__init__()
        self._prev_shoulder_x = None

    def update(self, landmarks) -> tuple[str, bool]:
        shoulder = landmarks["left_shoulder"]
        elbow = landmarks["left_elbow"]
        wrist = landmarks["left_wrist"]

        angle = calculate_angle(shoulder, elbow, wrist)
        feedback, good_form = "Good form! Keep it up.", True

        # Rep counting
        if angle > 160:
            self.stage = "down"
        if angle < 40 and self.stage == "down":
            self.stage = "up"
            self.reps += 1

        # Form check: shoulder should not swing forward significantly
        if self._prev_shoulder_x is not None:
            swing = abs(shoulder[0] - self._prev_shoulder_x)
            if swing > 0.03:
                feedback = "Control the swing — isolate the bicep!"
                good_form = False

        self._prev_shoulder_x = shoulder[0]
        return feedback, good_form
