from gensim import corpora,similarities,models
import os

class MusicSearcher():
    def __init__(self):
        self.dictionary = corpora.Dictionary.load('search_model/tfidf_dict.dict')
        self.tfidf = models.LsiModel.load('search_model/tfidf_model.model')
        self.index = similarities.SparseMatrixSimilarity.load('search_model/tfidf_index.index')
        self.dict_list=[]
        self.music_path=[]
        self.__set_music_path()
        for i in range(len(self.dictionary)):
            self.dict_list.append(self.dictionary[i])

    def __search_index(self,query):
        query=query.lower().split(" ")
        word=[]
        for q in query: #先檢查英文字(英文字經過token可以直接在dict查詢)
            if q in self.dict_list:
                word.append(q)
                query.pop(query.index(q)) #檢查過後將其pop(避免重複查詢)
        for w in self.dict_list: #檢查中文(中文因為沒經過切詞，因此改檢查dict是否存在於query內)
            for q in query:
                if w in q: word.append(w)
        query_bow = self.dictionary.doc2bow(word)
        tfidf_vec = self.tfidf[query_bow]
        sims = self.index[tfidf_vec]
        sorted_index = sorted(enumerate(sims), key=lambda item: -item[1])
        return sorted_index
        
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
    play_list=ms.get_play_list("afterglow easy come")
    print(play_list[:3])