class IntentRecongizer():
    def check_intent(self,text):
        print(text)
        if "播放" in text:
            text = text.partition("播放")
            toplay = text[0]+text[2]
            return "play", toplay
        elif "play" in text:
            text = text.partition("play")
            toplay = text[0]+text[2]
            return "play", toplay
        elif "暫停" in text:
            return "pause",""
        elif "pause" in text:
            return "pause",""
        elif "停止" in text:
            return "stop",""
        elif "stop" in text:
            return "stop",""
        elif "下一首" in text:
            return "next",""
        elif "next" in text:
            return "next",""
        else:
            return "",""