import numpy as np
import ast
import os

class MusicSearcher():
    def __init__(self):
        #存取id轉換表
        f=open("search_model\id_dict.txt","r")
        contents=f.read()
        self.id_dict=ast.literal_eval(contents)
        f.close()
        #存取idf
        f=open("search_model\idf.txt","r")
        contents=f.read()
        self.idf=ast.literal_eval(contents)
        f.close()
        #存取資料庫向量
        self.data_vector=np.load("search_model/data_vector.npy",allow_pickle=True)

        self.music_path=[]
        self.__set_music_path()

    def __search_index(self,query):
        query=query.lower()
        word=[]
        for w in self.id_dict.keys(): #檢查query有哪些詞在資料庫
            if w in query:
                addFlag=True #標記是否加入query的token
                for cw in word: #檢查是否已經有較完整詞語加入，若有，當前詞不加入 (cw => candidate word)
                    if w in cw:
                        addFlag=False
                        break
                if addFlag: word.append(w)
        word_id=[] #轉成id
        for w in word:
            word_id.append(self.id_dict[w])
        #計算query的vector
        word_v={} #紀錄向量
        for wid in word_id:
            word_v[wid]=word_v.get(wid,0)+1 #紀錄每個word出現次數
        for wid in word_v.keys(): #計算向量權重
            word_v[wid]=(word_v[wid]/len(self.data_vector))*self.idf[wid] #tf(weight) * idf
        #計算相似度
        sims=[] #紀錄相似度
        for v in self.data_vector:
            sims.append(self.__sim_compute(word_id,word_v,v))
        sorted_index = sorted(enumerate(sims), key=lambda item: -item[1])
        return sorted_index
    
    def __sim_compute(self,query_id,query_v,v): #計算cosine similarity
        nmr=0 #分子
        dmr=0 #分母
        for qid in query_id:
            if qid in v.keys():
                nmr += query_v[qid]*v[qid]
        q_dmr=0
        for i in query_v.keys():
            q_dmr += query_v[i]**2
        v_dmr=0
        for i in v.keys():
            v_dmr += v[i]**2
        dmr=q_dmr**(1/2)+v_dmr**(1/2)
        if dmr==0: return 0 #分母若為0回傳0
        return nmr/dmr
        
    def __set_music_path(self):
        folder_path = "music_prepare/path"
        allNameFile=os.listdir(folder_path)
        for filename in allNameFile:
            f = open(folder_path+"/"+filename,mode="r")
            for line in f:
                self.music_path.append(line[:-1])
            f.close()
    
    def get_play_list(self,query):
        index=self.__search_index(query)
        play_list=[]
        for i in range(len(index)):
            play_list.append(self.music_path[index[i][0]])
        return play_list

if __name__ == "__main__":
    ms=MusicSearcher()
    play_list=ms.get_play_list("一口氣全唸對")
    print(play_list[:3])