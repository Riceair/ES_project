import pygame

class MusicControl:
    def __init__(self):
        self.music_list=[]
        self.isPlaying=False
        self.isPause=False
        self.pg_mixer=pygame.mixer

    def set_music_list(self,music_list):
        self.music_list=music_list

    def add_music(self,music):
        self.music_list.append(music)

    def clear_music_list(self):
        self.music_list.clear()

    def music_play(self):
        if len(self.music_list)==0:
            return
        self.pg_mixer.init()
        self.pg_mixer.music.load(self.music_list.pop(0)) #將歌單第一首歌取出
        self.isPlaying=True
        self.pg_mixer.music.play()

    def music_pause(self): #暫停音樂
        if self.isPlaying==False: #若非播放音樂中，返回
            return
        if self.isPause==False: #若非暫停則暫停
            self.pg_mixer.music.pause()
            self.isPause=True
        elif self.isPause==True: #若為暫停則停止暫停
            self.pg_mixer.music.unpause()
            self.isPause=False

    def music_next(self): #播放下一首音樂
        self.pg_mixer.music.stop()
        self.isPlaying=False
        self.isPause=False
        self.music_play()

    def music_stop(self): #所有音樂停止播放
        self.pg_mixer.music.stop()
        self.isPlaying=False
        self.isPause=False
        self.clear_music_list()

if __name__ == "__main__":
    mc=MusicControl()
    mc.set_music_list(["D:/..music_data/J-Pop/ClariS-ClariS - Single Best 1st-09-Click.mp3","D:/..music_data/Anime/Afterglow-Easy Come, Easy Go! - Single-01-Easy Come, Easy Go!.mp3"])
    mc.music_play()
    while True:
        chose=input("Press 1 to pause/unpause, 2 to next, 3 to stop:\n")
        if chose==str(1):
            mc.music_pause()
        elif chose==str(2):
            mc.music_next()
        elif chose==str(3):
            mc.music_stop()
            break