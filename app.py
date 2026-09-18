import streamlit as st
from pathlib import Path
import subprocess
import sys

# Page configuration
st.set_page_config(
    page_title="AI Music Generator",
    page_icon="🎵",
    layout="centered"
)

# Custom styling
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 18px;
    margin-bottom: 30px;
}

.info-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #f5f5f5;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<div class="main-title">🎵 AI Music Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Generate new music using an LSTM deep learning model</div>',
    unsafe_allow_html=True
)

# Project information
st.markdown("""
<div class="info-box">
<b>🤖 Model:</b> LSTM Neural Network<br>
<b>🎼 Dataset:</b> MIDI Music Collection<br>
<b>🐍 Technology:</b> Python + TensorFlow + Music21
</div>
""", unsafe_allow_html=True)

# Generation settings
st.subheader("🎼 Music Generation")

num_notes = st.slider(
    "Number of musical notes to generate",
    min_value=50,
    max_value=200,
    value=100,
    step=10
)

st.write(f"Selected: **{num_notes} musical elements**")

# Generate button
if st.button("🎵 Generate New Music", use_container_width=True):

    with st.spinner("AI is composing your music... 🎶"):

        try:
            # Run the existing music generation script
            result = subprocess.run(
                [sys.executable, "generate_music.py", str(num_notes)],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:

                output_file = Path("output/generated_music.mid")

                st.success("🎉 Music generated successfully!")

                if output_file.exists():

                    st.subheader("🎧 Generated Music")

                    st.info(
                        "Your generated MIDI file is ready. "
                        "Download it and open it with a MIDI-compatible player."
                    )

                    with open(output_file, "rb") as file:
                        st.download_button(
                            label="⬇️ Download Generated MIDI",
                            data=file,
                            file_name="generated_music.mid",
                            mime="audio/midi",
                            use_container_width=True
                        )

                else:
                    st.error("Generated MIDI file was not found.")

            else:
                st.error("Music generation failed.")
                st.code(result.stderr)

        except Exception as error:
            st.error(f"Error: {error}")

# Footer
st.markdown("---")

st.caption(
    "CodeAlpha Artificial Intelligence Internship • "
    "Task 3: Music Generation with AI"
)

st.caption("Author: SATYA PRIYA")