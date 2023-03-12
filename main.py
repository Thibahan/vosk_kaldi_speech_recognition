from utils import record_audio
from model import load_model, get_results
import wave

# Filename for audio recording
recording = 'recording.wav'

# Name of the model
model_name = "vosk-model-de-0.21"

# Record microphone input for [seconds]
seconds = 5
record_audio(seconds, recording)

# Open recoreded wav file
wf = wave.open(recording, "rb")

# Load model and get results of recognizer
recognizer = load_model(wf.getframerate(), model_name=model_name)
results = get_results(wf, recognizer)

# Get text from results dict and split into words
results = results["text"]
words = results.split(" ")

# Print the words
print(words)
