import os
from os import walk
import pandas as pd

dataDir = "./data/output"
allFiles = next(walk(dataDir), (None, None, []))[2]
print("载入原始数据完毕，数据量", len(allFiles))
# 加载原始数据
frames = []
for i in range(len(allFiles)):
    file = allFiles[i]
    print(file)
    frames.append(pd.read_csv("./data/output/"+file, sep="`",header=None, names=["sentence"]))
df = pd.concat(frames, axis=0, ignore_index=True)

# 加载模型，将数据进行向量化处理
from sentence_transformers import SentenceTransformer
if os.path.exists('uer_sbert-base-chinese-nli'):
    model = SentenceTransformer('/Users/lijunjun/PycharmProjects/faiss-demo/uer_sbert-base-chinese-nli')
    dimension = model.get_sentence_embedding_dimension()
else:
    model = SentenceTransformer('uer/sbert-base-chinese-nli')
    model.save("/Users/lijunjun/PycharmProjects/faiss-demo/uer_sbert-base-chinese-nli")
sentences = df['sentence'].tolist()
sentence_embeddings = model.encode(sentences)

# 将向量处理结果存储
import numpy as np
save_file = "data.npy"
np.save(save_file, sentence_embeddings)

file_size = os.path.getsize(save_file)
print("%7.3f MB" % (file_size/1024/1024))

print("prepare 结束")