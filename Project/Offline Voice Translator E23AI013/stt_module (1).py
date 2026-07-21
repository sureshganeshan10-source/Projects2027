import sounddevice as sd
import queue, json
from vosk import Model, KaldiRecognizer

def main():
    # Load Hindi Vosk model (adjust path if needed)
    model = Model("model/vosk-model-small-hi-0.22")
    rec = KaldiRecognizer(model, 16000)
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status, flush=True)
        q.put(bytes(indata))

    print("Recording... Speak now!")

    # Open microphone stream
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                print("You said:", text)
                with open("output.txt", "w", encoding="utf-8") as f:
                    f.write(text)
                print("Saved to output.txt")
                break

if __name__ == "__main__":
    main()
