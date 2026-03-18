"""
Streamlit web UI for AI Fitness Coach.
Uses st.camera_input — works on Streamlit Cloud with no WebRTC dependencies.
"""
import cv2
import numpy as np
import streamlit as st

from pose_detector import PoseDetector
from exercises import EXERCISES
from utils.drawing import draw_rep_counter, draw_feedback

st.set_page_config(page_title="AI Fitness Coach", layout="wide")
st.title("AI Fitness Coach")
st.caption("Select an exercise, allow camera access, then capture a frame to analyze your form.")

# Persist rep count and stage across captures
if "reps" not in st.session_state:
    st.session_state.reps = 0
if "stage" not in st.session_state:
    st.session_state.stage = None
if "prev_exercise" not in st.session_state:
    st.session_state.prev_exercise = None

col1, col2 = st.columns([3, 1])

with col2:
    exercise_name = st.selectbox("Exercise", list(EXERCISES.keys()), format_func=str.capitalize)

    # Reset when exercise changes
    if st.session_state.prev_exercise != exercise_name:
        st.session_state.reps = 0
        st.session_state.stage = None
        st.session_state.prev_exercise = exercise_name

    st.markdown("### Stats")
    reps_slot = st.empty()
    stage_slot = st.empty()
    reps_slot.metric("Reps", st.session_state.reps)
    stage_slot.metric("Stage", st.session_state.stage or "—")

    if st.button("Reset Reps"):
        st.session_state.reps = 0
        st.session_state.stage = None
        st.rerun()

    st.divider()
    st.markdown("**Tips:**")
    st.markdown("- Stand 2–3 m from the camera")
    st.markdown("- Ensure full body is in frame")
    st.markdown("- Capture at the top and bottom of each rep")

with col1:
    frame_file = st.camera_input("Webcam — click capture to analyze")
    result_slot = st.empty()

if frame_file is not None:
    # Decode JPEG → BGR numpy array
    nparr = np.frombuffer(frame_file.getvalue(), np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Restore exercise state from session
    exercise = EXERCISES[exercise_name]()
    exercise.reps = st.session_state.reps
    exercise.stage = st.session_state.stage

    detector = PoseDetector()
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
    detector.close()

    # Save updated state back to session
    st.session_state.reps = exercise.reps
    st.session_state.stage = exercise.stage

    # Refresh stats
    reps_slot.metric("Reps", st.session_state.reps)
    stage_slot.metric("Stage", st.session_state.stage or "—")

    # Show annotated frame (BGR → RGB for st.image)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result_slot.image(frame_rgb, channels="RGB", use_container_width=True)
