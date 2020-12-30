class SoundDetector:
    def __init__(self):
        self.num_samples = 2000    #pyaudio內建緩衝大小
        self.sampling_rate = 8000  #取樣頻率
        self.level = 15000          #聲音儲存的閾值
        self.isListen=False