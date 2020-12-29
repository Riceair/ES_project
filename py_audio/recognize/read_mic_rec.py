import speech_recognition
import pyaudio
import os
import sys
import wave
import numpy as np 
from pyaudio import PyAudio, paInt16
class GenAudio(object):
    def __init__(self):
        self.num_samples = 2000    #pyaudio內建緩衝大小
        self.sampling_rate = 8000  #取樣頻率
        self.level = 10000          #聲音儲存的閾值
        self.count_num = 20        #count_num個取樣之內出現COUNT_NUM個大於LEVEL的取樣則記錄聲音
        self.save_length = 8       #聲音記錄的最小長度：save_length * num_samples 個取樣
        self.voice_string = []
        self.isListen=False
    
    #儲存檔案
    def save_wav(self, filename):
        wf = wave.open(filename, "wb") 
        wf.setnchannels(1) 
        wf.setsampwidth(2) 
        wf.setframerate(self.sampling_rate) 
        wf.writeframes(np.array(self.voice_string).tostring())
        wf.close()
    
    
    def read_audio(self):
        pa = PyAudio() 
        stream = pa.open(format=paInt16, channels=1, rate=self.sampling_rate, input=True, 
                frames_per_buffer=self.num_samples) 
        
        r = speech_recognition.Recognizer()
        
        save_count = 0
        save_buffer = []
        while True:            
            # 讀入num_samples個取樣
            string_audio_data = stream.read(self.num_samples)

            # 將讀入的資料轉換為陣列
            audio_data = np.fromstring(string_audio_data, dtype = np.short)
            #計算大於 level 的取樣的個數
            large_sample_count = np.sum(audio_data > self.level)
            if large_sample_count>0:
                self.isListen=True
                save_buffer.append(string_audio_data)
            else: #取樣結束
                if self.isListen:
                    self.isListen=False
                    if len(save_buffer)==1:
                        continue
                    with speech_recognition.Microphone() as source: 
                        print("Please talk:")
                        r.adjust_for_ambient_noise(source) # 函數調整麥克風的噪音:
                        audio = r.listen(source)
                    try:
                        Text = r.recognize_google(audio, language="zh-TW")
                        print(Text)
                    except:
                        print("error")
                    save_buffer.clear()
                
        return True
if __name__ == "__main__":
    r = GenAudio()
    r.read_audio()
    r.save_wav("./test.wav")


# r = speech_recognition.Recognizer()
# with speech_recognition.Microphone() as source: 
#     print("Please talk:")
#     r.adjust_for_ambient_noise(source) # 函數調整麥克風的噪音:
#     audio = r.listen(source)
# try:
#     Text = r.recognize_google(audio, language="zh-TW")
#     print(Text)
# except:
#     print("error")