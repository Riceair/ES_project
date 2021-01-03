from gensim import corpora,similarities,models
import os,re

folder_path = "music_prepare/name"
allNameFile=os.listdir(folder_path)

music_tokens=[]
for filename in allNameFile:
    f = open(folder_path+"/"+filename,mode="r")
    c=0 #紀錄一個類別有多少首歌
    for line in f:
        c+=1
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
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=100) #建立Lsi model
index=similarities.MatrixSimilarity(lsi[corpus]) #紀錄相似度index

#儲存model dict index
dictionary.save("search_model/Lsi_dict.dict")
lsi.save("search_model/Lsi_model.lsi")
index.save("search_model/Lsi_index.index")

#產生jieba字詞表
f=open("search_model/jieba_dict.txt",mode="w")
for i in range(len(dictionary)):
    f.write(dictionary[i]+"\n")
f.close()