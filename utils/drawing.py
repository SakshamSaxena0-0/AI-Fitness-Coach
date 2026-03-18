import cv2


def draw_rep_counter(frame, reps, stage, exercise_name):
    """Draw rep counter and stage box in the top-left corner."""
    # Background box
    cv2.rectangle(frame, (0, 0), (240, 90), (245, 117, 16), -1)

    # Exercise name
    cv2.putText(frame, exercise_name.upper(), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    # Labels
    cv2.putText(frame, 'REPS', (15, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, 'STAGE', (105, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    # Values
    cv2.putText(frame, str(reps), (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, stage or '-', (100, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)


def draw_feedback(frame, feedback, good_form):
    """Draw form feedback text at the bottom of the frame."""
    h, w = frame.shape[:2]
    color = (0, 200, 0) if good_form else (0, 0, 220)
    cv2.rectangle(frame, (0, h - 50), (w, h), color, -1)
    cv2.putText(frame, feedback, (10, h - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)


def draw_angle(frame, point, angle):
    """Draw angle value near a joint."""
    cv2.putText(frame, f"{int(angle)}°", tuple(map(int, point)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
