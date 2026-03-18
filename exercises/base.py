class Exercise:
    name = "exercise"

    def __init__(self):
        self.reps = 0
        self.stage = None  # "up" or "down"

    def update(self, landmarks) -> tuple[str, bool]:
        """
        Process landmarks, update rep count and stage.
        Returns (feedback_text, is_good_form).
        """
        raise NotImplementedError

    def reset(self):
        self.reps = 0
        self.stage = None
