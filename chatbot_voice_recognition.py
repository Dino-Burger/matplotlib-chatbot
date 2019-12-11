from deepspeech import Model
import numpy as np
import speech_recognition as sr

sample_rate = 16000
beam_width = 500

if __name__ == '__main__':
    ds = Model("deepspeech-0.6.0-models/output_graph.pbmm", 500)

    r = sr.Recognizer()
    with sr.Microphone(sample_rate=sample_rate) as source:
        print("Say Something")
        audio = r.listen(source)
        audio = np.frombuffer(audio.frame_data, np.int16)

    print(ds.stt(audio))
