import argparse
import cv2
from pose_detector import PoseDetector
from exercises import EXERCISES
from utils.drawing import draw_rep_counter, draw_feedback


def run(exercise_name: str, camera_index: int = 0):
    if exercise_name not in EXERCISES:
        print(f"Unknown exercise '{exercise_name}'. Choose from: {list(EXERCISES.keys())}")
        return

    exercise = EXERCISES[exercise_name]()
    detector = PoseDetector()
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print(f"Starting {exercise_name} tracker. Press 'q' to quit, 'r' to reset reps.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # mirror view
        landmarks, results = detector.detect(frame)

        feedback, good_form = "Stand in frame to begin.", True

        if landmarks:
            try:
                feedback, good_form = exercise.update(landmarks)
            except KeyError:
                feedback = "Make sure full body is visible."
                good_form = False

        detector.draw_landmarks(frame, results)
        draw_rep_counter(frame, exercise.reps, exercise.stage, exercise_name)
        draw_feedback(frame, feedback, good_form)

        cv2.imshow(f"AI Fitness Coach — {exercise_name.capitalize()}", frame)

        key = cv2.waitKey(10) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            exercise.reset()
            print("Reps reset.")

    cap.release()
    cv2.destroyAllWindows()
    detector.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Fitness Coach")
    parser.add_argument(
        "--exercise", type=str, default="squat",
        choices=list(EXERCISES.keys()),
        help="Exercise to track (default: squat)"
    )
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
    args = parser.parse_args()
    run(args.exercise, args.camera)
