import sounddevice as sd
import queue
import sys
import json

from model import load_model


class live_recognizer():
    """Live speech to text recognizer. This class will record your
    microphone and print out the text.

    Args:
        model_name (str, optional): Name of the model. Defaults to "vosk-model-de-0.21".
        samplerate (int, optional): Samplerate of audio input. Defaults to 44100.
        device (int, optional): Device number.
        Use python -m sounddevice to get number. Defaults to 1.
    """

    def __init__(self, model_name: str = "vosk-model-de-0.21",
                 samplerate: int = 44100, device: int = 1):
        """Init class"""
        self.model_name = model_name

        self.samplerate = samplerate
        self.device = device

        self.q = queue.Queue()

        self.old_res = ""

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def recognize_live(self):

        with sd.RawInputStream(samplerate=self.samplerate, blocksize=8000, device=self.device,
                               dtype="int16", channels=1, callback=self.callback):
            print("#" * 80)
            print("Press Ctrl+C to stop the recording")
            print("#" * 80)

            recognizer = load_model(
                self.samplerate, model_name=self.model_name)
            while True:
                data = self.q.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())["text"]
                else:
                    result = json.loads(recognizer.PartialResult())["partial"]

                if result != "" and result != self.old_res:
                    print(result)
                self.old_res = result


if __name__ == '__main__':
    rec = live_recognizer()
    rec.recognize_live()
