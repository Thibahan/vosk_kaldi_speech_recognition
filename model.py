import json
from wave import Wave_read
from vosk import Model, KaldiRecognizer
from vosk import SetLogLevel
SetLogLevel(-1)


def load_model(frame_rate: int, model_name: str = "vosk-model-small-de-0.15") -> KaldiRecognizer:
    """This function will load a vosk model with a KaldiRecognizer.
    Check documentations of recognizer here: https://kaldi-asr.org/doc/

    Args:
        frame_rate (int): Framerate of input.
        model_name (str, optional): Name if the model/Path to model.
        Defaults to "vosk-model-small-de-0.15".

    Returns:
        KaldiRecognizer: Returns a Vosk Kaldi recognizer
    """
    model = Model(model_name)
    recognizer = KaldiRecognizer(model, frame_rate)
    recognizer.SetWords(True)
    return recognizer


def get_results(wave_object: Wave_read, recognizer: KaldiRecognizer,
                n_frames: int = 4000) -> dict:
    """This function will iterate over wave_read object an recognize text.

    Args:
        wave_object (Wave_read): Wave object with audio to get text of.
        recognizer (KaldiRecognizer): Recognizer of loaded modell.
        n_frames (int, optional): Number of frames to iterate.
        Defaults to 4000.

    Returns:
        dict: Dictionary with the results of the recognizer.
    """
    while True:
        data = wave_object.readframes(n_frames)
        if len(data) == 0:
            break
        recognizer.AcceptWaveform(data)

    results = recognizer.FinalResult()
    results = json.loads(results)
    return results
