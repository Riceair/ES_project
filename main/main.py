from MusicControler import MusicControler
from SpeechRecongizer import SpeechRecongizer
from IntentRecongizer import IntentRecongizer
from MusicSearcher import MusicSearcher
import pyaudio
import os
import numpy as np
import wave
from pyaudio import PyAudio, paInt16

num_samples = 2000    #pyaudio內建緩衝大小
sampling_rate = 8000  #取樣頻率
level = 15000          #聲音儲存的閾值
ass_wake="狗"
isPlaying=False
save_count = 0
save_buffer = []
calling_wav_name="main/isCalling.wav"
isListen=False

def save_wav(sampling_rate, voice_string,filename):
        wf = wave.open(filename, "wb") 
        wf.setnchannels(1) 
        wf.setsampwidth(2) 
        wf.setframerate(sampling_rate) 
        wf.writeframes(np.array(voice_string).tostring())
        wf.close()

pa = PyAudio() 
stream = pa.open(format=paInt16, channels=1, rate=sampling_rate, input=True, 
        frames_per_buffer=num_samples) 

#物件
mc=MusicControler()
ms=MusicSearcher()
sr=SpeechRecongizer()
ir=IntentRecongizer()

while True:
    if isPlaying and mc.is_busy()==False: mc.music_next() #檢測是否結束播放一首歌
    # 讀入num_samples個取樣
    string_audio_data = stream.read(num_samples)

    # 將讀入的資料轉換為陣列
    audio_data = np.fromstring(string_audio_data, dtype = np.short)
    #計算大於 level 的取樣的個數
    large_sample_count = np.sum(audio_data > level)
    if large_sample_count>0:
        isListen=True
        save_buffer.append(string_audio_data)
    else: #取樣結束
        if isListen:
            isListen=False
            if len(save_buffer)==1:
                continue
            #開始辨識是否被呼叫
            save_wav(sampling_rate,save_buffer,calling_wav_name)
            Text=sr.isCalling_recongize(calling_wav_name)
            if Text==-1:
                print("I'm not sure")
                continue
            else:
                if ass_wake in Text:
                    #辨識意圖
                    save_buffer.clear()
                    print("What's your intent?")
                    if isPlaying and mc.get_isPause()==False: mc.music_pause() #若正在播放先暫停 (若為暫停狀態則忽視)
                    Text=sr.start_recongize()
                    if Text==-1:
                        if isPlaying: mc.music_pause() #若正在播放則繼續播放
                        continue
                    else: #確認
                        intent,play_name = ir.check_intent(Text)
                        if intent=="": continue
                        if not isPlaying and intent=="play":
                            mc.set_music_list(ms.get_play_list(play_name))
                            mc.music_play()
                            isPlaying=True
                        elif isPlaying:
                            if intent=="pause":
                                #pause music
                                continue
                            elif intent=="play":
                                mc.music_pause()
                            elif intent=="stop":
                                #stop music
                                mc.music_stop()
                                isPlaying=False
                            elif intent=="next":
                                mc.music_next()
            save_buffer.clear()