import os
import sys
import wave
import numpy as np 
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
        time_count = self.time_count
        while True:
            time_count -= 1
            
            # 讀入num_samples個取樣
            string_audio_data = stream.read(self.num_samples)     
            # 將讀入的資料轉換為陣列
            audio_data = np.fromstring(string_audio_data, dtype = np.short)
            #計算大於 level 的取樣的個數
            large_sample_count = np.sum(audio_data > self.level)
            
            print(np.max(audio_data)),  "large_sample_count=>", large_sample_count
            # 如果個數大於COUNT_NUM，則至少儲存SAVE_LENGTH個塊
            if large_sample_count > self.count_num:
                save_count = self.save_length
            else: 
                save_count -= 1
            if save_count < 0:
                save_count = 0
            
            if save_count > 0:
                save_buffer.append(string_audio_data)
            else:
                if len(save_buffer) > 0:
                    self.voice_string = save_buffer
                    save_buffer = [] 
                    print("Recode a piece of  voice successfully!")
                    return True
            
            if time_count == 0: 
                if len(save_buffer) > 0:
                    self.voice_string = save_buffer
                    save_buffer = []
                    print("Recode a piece of  voice successfully!")
                    return True
                else:
                    return False
        return True
if __name__ == "__main__":
    r = GenAudio()
    r.read_audio()
    r.save_wav("./test.wav")