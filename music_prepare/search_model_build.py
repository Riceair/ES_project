import numpy as np
import os,re
import math

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

#將詞轉成id，並記錄詞語出現在的文件數
id_dict={} #儲存轉換過的id (to save)
all_idf={} #紀錄idf (to save)
the_id=0
for token in music_tokens:
    for t in token:
        if len(t)==1 or t.isdigit(): continue
        if t not in id_dict.keys():
            id_dict[t]=the_id #設定token的id
            all_idf[the_id]=0 #初始化要紀錄的詞
            the_id=the_id+1 #id加一
    token_set=list(set(token)) #去除重複的詞
    for ts in token_set: #紀錄詞的檔案頻率
        if len(ts)==1 or ts.isdigit(): continue
        all_idf[id_dict[ts]]+=1

for idf in all_idf: #計算idf
    all_idf[idf]=math.log(len(music_tokens)/all_idf[idf])

music_vector=[] #儲存每首歌檔名轉換的向量 (to save)
for token in music_tokens:
    v_dict={} #紀錄稀疏向量的dict
    for t in token:
        if len(t)==1 or t.isdigit(): continue
        t2id=id_dict[t] #將詞轉成id
        v_dict[t2id]=v_dict.get(t2id,0)+1 #計算詞在該歌曲名稱的數量
    for wid in v_dict.keys():
        v_dict[wid]=(v_dict[wid]/(len(token)))*all_idf[wid] #計算tf * idf
    music_vector.append(v_dict)
music_vector=np.array(music_vector) #轉成np array (save使用)

f=open("search_model/id_dict.txt","w") #儲存詞語轉id的dict
f.write(str(id_dict))
f.close()

f=open("search_model/idf.txt","w") #儲存idf
f.write(str(all_idf))
f.close()

np.save("search_model/data_vector",music_vector)