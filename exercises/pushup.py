from .base import Exercise
from utils.angles import calculate_angle


class Pushup(Exercise):
    name = "pushup"

    def update(self, landmarks) -> tuple[str, bool]:
        shoulder = landmarks["left_shoulder"]
        elbow = landmarks["left_elbow"]
        wrist = landmarks["left_wrist"]
        hip = landmarks["left_hip"]
        ankle = landmarks["left_ankle"]

        elbow_angle = calculate_angle(shoulder, elbow, wrist)
        body_angle = calculate_angle(shoulder, hip, ankle)
        feedback, good_form = "Good form! Keep it up.", True

        # Rep counting
        if elbow_angle < 90:
            self.stage = "down"
        if elbow_angle > 160 and self.stage == "down":
            self.stage = "up"
            self.reps += 1

        # Form checks — body should be roughly straight (160–200°)
        if body_angle < 155:
            feedback = "Raise your hips — keep body straight!"
            good_form = False
        elif body_angle > 200:
            feedback = "Lower your hips — keep body straight!"
            good_form = False

        return feedback, good_form
