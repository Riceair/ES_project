import speech_recognition
import os
import pyaudio

class SpeechRecongizer:
    def __init__(self):
        self.r=speech_recognition.Recognizer()

    def start_recongize(self):
        with speech_recognition.Microphone() as source: 
            self.r.adjust_for_ambient_noise(source) # 函數調整麥克風的噪音:
            audio = self.r.listen(source)
        try:
            Text = self.r.recognize_google(audio, language="zh-TW")
            return Text
        except:
            return -1

if __name__ == "__main__":
    sr=SpeechRecongizer()
    print(sr.start_recongize())