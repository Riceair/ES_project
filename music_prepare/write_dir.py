import os

original_path = "D:/..music_data"
allFolder=os.listdir(original_path)
allfList=[]
#將所有的歌曲讀入
for i in range(len(allFolder)):
    myPath=original_path+"/"+allFolder[i]
    fList=[]
    for file in os.listdir(myPath):
        fList.append(file)
    allfList.append(fList)

data_path="path"
folder=os.path.exists(data_path)
if not folder:
    os.makedirs(data_path)
#將所有音檔的路徑寫成txt
for i in range(len(allFolder)):
    f=open(data_path+"/"+allFolder[i]+".txt","w")
    for ms_n in allfList[i]:
        f.write(original_path+"/"+allFolder[i]+"/"+ms_n+"\n")
    f.close()

name_path="name"
folder=os.path.exists(name_path)
if not folder:
    os.makedirs(name_path)
#將音檔名紀錄(建立向量模型用)
for i in range(len(allFolder)):
    f=open(name_path+"/"+allFolder[i]+".txt","w")
    for ms_n in allfList[i]:
        f.write(ms_n[:-4]+"\n")
    f.close()