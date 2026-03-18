from .base import Exercise
from utils.angles import calculate_angle


class Squat(Exercise):
    name = "squat"

    def update(self, landmarks) -> tuple[str, bool]:
        # Key joints (using left side)
        hip = landmarks["left_hip"]
        knee = landmarks["left_knee"]
        ankle = landmarks["left_ankle"]

        angle = calculate_angle(hip, knee, ankle)
        feedback, good_form = "Good form! Keep it up.", True

        # Rep counting
        if angle < 90:
            self.stage = "down"
        if angle > 160 and self.stage == "down":
            self.stage = "up"
            self.reps += 1

        # Form checks
        if knee[0] > ankle[0] + 0.05:  # knee past toes (normalized coords)
            feedback = "Keep knees behind toes!"
            good_form = False
        elif angle < 60:
            feedback = "Too deep — stop at parallel."
            good_form = False

        return feedback, good_form
