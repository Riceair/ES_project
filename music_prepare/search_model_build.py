from gensim import corpora,similarities,models
import os,re

folder_path = "music_prepare/name"
allNameFile=os.listdir(folder_path)

music_tokens=[]
for filename in allNameFile:
    f = open(folder_path+"/"+filename,mode="r")
    for line in f:
        line=re.sub(r'[^\w\s]|\n'," ",line) #將標點符號以空格替換
        line=line.lower().split(" ") #轉小寫並用依照空格分開
        token=[] #紀錄歌曲的token
        for word in line:
            if word=="": continue #去除空白token
            token.append(word)
        music_tokens.append(token)
    f.close()

#將字詞轉成id
dictionary=corpora.Dictionary(music_tokens)
corpus=[dictionary.doc2bow(w) for w in music_tokens]  #計算每一個字出現頻率 並轉為bow(稀疏向量形式)
tfidf=models.TfidfModel(corpus) #把bow輸入進入tfidf
index=similarities.MatrixSimilarity(tfidf[corpus]) #紀錄相似度index

#儲存model dict index
dictionary.save("search_model/tfidf_dict.dict")
tfidf.save("search_model/tfidf_model.model")
index.save("search_model/tfidf_index.index")