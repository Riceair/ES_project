import os
import sys
import wave
import numpy as np
from SpeechRecongizer import SpeechRecongizer
from pyaudio import PyAudio, paInt16
class GenAudio(object):
    def __init__(self):
        self.num_samples = 2000    #pyaudio內建緩衝大小
        self.sampling_rate = 8000  #取樣頻率
        self.level = 1500          #聲音儲存的閾值
        self.count_num = 20        #count_num個取樣之內出現COUNT_NUM個大於LEVEL的取樣則記錄聲音
        self.save_length = 8       #聲音記錄的最小長度：save_length * num_samples 個取樣
        self.time_count = 8        #錄音時間，單位s
        self.voice_string = []
    
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
        
        save_count = 0
        save_buffer = []
        isListen=False
        sr=SpeechRecongizer()
        while True:            
            # 讀入num_samples個取樣
            string_audio_data = stream.read(self.num_samples)     
            # 將讀入的資料轉換為陣列
            audio_data = np.fromstring(string_audio_data, dtype = np.short)
            #計算大於 level 的取樣的個數
            large_sample_count = np.sum(audio_data > self.level)
            
            if large_sample_count>0:
                isListen=True
                save_buffer.append(string_audio_data)
            else: #取樣結束
                if isListen:
                    isListen=False
                    if len(save_buffer)==1:
                        continue
                    #開始辨識是否被呼叫
                    self.voice_string=save_buffer
                    self.save_wav('test.wav')
                    #Text=sr.start_recongize()
                    print(sr.isCalling_recongize('test.wav'))
                save_buffer.clear()
        return True
if __name__ == "__main__":
    r = GenAudio()
    r.read_audio()