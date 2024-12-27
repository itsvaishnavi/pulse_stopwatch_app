import streamlit as st
import time
from datetime import timedelta

# App title
st.title("Pulse: Your online Stopwatch App")

# Initialize session state variables
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "elapsed_time" not in st.session_state:
    st.session_state.elapsed_time = 0.0
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "start_disabled" not in st.session_state:
    st.session_state.start_disabled = False
if "stop_disabled" not in st.session_state:
    st.session_state.stop_disabled = True

# Function to format elapsed time in hh:mm:ss.milliseconds format
def format_time(elapsed_time):
    delta = timedelta(seconds=elapsed_time)
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int(delta.microseconds / 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

# Function to start the stopwatch
def start_stopwatch():
    if not st.session_state.is_running:
        st.session_state.start_time = time.time() - st.session_state.elapsed_time
        st.session_state.is_running = True
        st.session_state.start_disabled = True
        st.session_state.stop_disabled = False

# Function to stop the stopwatch
def stop_stopwatch():
    if st.session_state.is_running:
        st.session_state.elapsed_time = time.time() - st.session_state.start_time
        st.session_state.is_running = False
        st.session_state.start_disabled = False
        st.session_state.stop_disabled = True

# Function to reset the stopwatch
def reset_stopwatch():
    st.session_state.start_time = None
    st.session_state.elapsed_time = 0.0
    st.session_state.is_running = False
    st.session_state.start_disabled = False
    st.session_state.stop_disabled = True

# Stopwatch controls
col1, col2, col3 = st.columns(3)

with col1:
    st.button("Start", on_click=start_stopwatch, disabled=st.session_state.start_disabled)

with col2:
    st.button("Stop", on_click=stop_stopwatch, disabled=st.session_state.stop_disabled)

with col3:
    st.button("Reset", on_click=reset_stopwatch)

# Display the stopwatch time
placeholder = st.empty()  # Placeholder for updating time

while True:
    if st.session_state.is_running:
        st.session_state.elapsed_time = time.time() - st.session_state.start_time

    # Display the updated time in hh:mm:ss.milliseconds format
    formatted_time = format_time(st.session_state.elapsed_time)
    placeholder.metric(label="Elapsed Time", value=formatted_time)

    # Break the loop if the stopwatch is not running
    if not st.session_state.is_running:
        break

    # Sleep briefly to avoid overloading the UI updates
    time.sleep(0.1)
