"""
This model listens to audio and runs it through both, 
the google online api as well as the mozilla offline model.
For the mozilla model you need deepspeech as well as 
the 1.2 GB file from 
https://github.com/mozilla/DeepSpeech/releases/download/v0.6.0/deepspeech-0.6.0-models.tar.gz
In my tests, google was better
"""


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
        audioInt16 = np.frombuffer(audio.frame_data, np.int16)

    print('mozilla', ds.stt(audioInt16))
    print('google', r.recognize_google(audio))
