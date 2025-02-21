import os
import tempfile

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import torchaudio
from audiocraft.models import JASCO
from audiorecorder import audiorecorder
from huggingface_hub import login
from dotenv import load_dotenv

load_dotenv()

# Login to Hugging Face Hub
if 'hf_logged_in' not in st.session_state:
    st.session_state.hf_logged_in = False
    st.session_state.model = None

if not st.session_state.hf_logged_in:
    login(os.environ.get("HF_KEY")) # Add Hugging Face API key to env
    st.session_state.hf_logged_in = True
    st.session_state.model = JASCO.get_pretrained(
        'facebook/jasco-chords-drums-melody-400M',
        chords_mapping_path='assets/chord_to_index_mapping.pkl',
    )
    st.session_state.model.set_generation_params(
        cfg_coef_all=1.5,
        cfg_coef_txt=0.5
    )

def plot_output_waveform(waveform, sample_rate):
    duration = waveform.shape[1] / sample_rate
    time_axis = np.linspace(0, duration, waveform.shape[1])
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(time_axis, waveform[0].cpu().numpy(), color='#1f77b4', alpha=0.7)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title('Generated Audio Waveform')
    ax.grid(True, alpha=0.3)
    return fig

def main():
    st.set_page_config(
        page_title="Deluloop",
        layout="wide"
    )
    st.image("assets/logo.png", caption="Generative Looper for Musicians", width=600)

    # Upload audio file
    audio_file = st.file_uploader("Upload a track (WAV)", type=['wav'])
    if audio_file:
        st.audio(audio_file, format='audio/wav')

    # Record audio
    recorded_audio = audiorecorder("Click to record", "Click to stop recording")
    if recorded_audio:
        exported_recorded_audio = recorded_audio.export()
        st.audio(exported_recorded_audio.read())

    # Add description
    description = st.text_input("Enter description", value="Synth Melody and Funky bassline")
    
    # Generate button with validation
    if st.button("Generate Music"):
        if audio_file is None:
            if recorded_audio is None:
                st.error("Please upload or record an audio file first!")
            else:
                process_audio(recorded_audio, description)
        elif not description.strip():
            st.error("Please enter a description!")
        else:
            process_audio(audio_file, description)

def process_audio(audio_file, description):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            tmp_file.write(audio_file.getvalue())
            tmp_path = tmp_file.name
    except Exception as e:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            tmp_path = temp_file.name
            audio_file.export(tmp_path, format="wav")

    try:
        # Load input audio
        waveform, sample_rate = torchaudio.load(tmp_path)

        with st.spinner('🎵 Generating music... this may take a few minutes...'):
            # Generate music
            chords = [('C', 0.0)]
            output = st.session_state.model.generate_music(
                descriptions=[description],
                drums_wav=waveform,
                drums_sample_rate=sample_rate,
                chords=chords,
                progress=True
            )
            asset_path = "assets/output.wav"
            torchaudio.save(asset_path, output[0].cpu(), sample_rate)
            st.audio(asset_path, loop=True)
            st.pyplot(plot_output_waveform(output[0], sample_rate))

    except Exception as e:
        st.error(f"Error processing audio file: {str(e)}")
    finally:
        os.unlink(tmp_path)

if __name__ == "__main__":
    main()
