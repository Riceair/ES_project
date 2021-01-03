from gensim import corpora,similarities,models

dictionary = corpora.Dictionary.load('search_model/Lsi_dict.dict')
lsi = models.LsiModel.load('search_model/Lsi_model.lsi')
index = similarities.SparseMatrixSimilarity.load('search_model/Lsi_index.index')

print(lsi)