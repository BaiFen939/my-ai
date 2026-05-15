import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
import chromadb
from sentence_transformers import SentenceTransformer
from datetime import datetime

# ---------- 初始化 ----------
# 1. 加载中文向量模型（第一次运行会自动下载，约400MB，稍等片刻）
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 2. 创建向量数据库客户端（数据会存在当前目录的 ./chroma_luoli 文件夹里）
client = chromadb.PersistentClient(path="./chroma_luoli")

# 3. 创建一个集合（相当于一张表），名字叫 luoli_memory
collection = client.get_or_create_collection(name="luoli_memory")

# ---------- 功能函数 ----------
def add_to_vector_memory(user_id, speaker, content, timestamp=None):
    """将一条对话存入向量数据库"""
    if timestamp is None:
        timestamp = datetime.now()
    # 生成向量
    embedding = model.encode(content).tolist()
    # 准备元数据（用于过滤用户）
    metadata = {
        "user_id": user_id,
        "speaker": speaker,
        "timestamp": timestamp.isoformat()
    }
    # 唯一ID
    doc_id = f"{user_id}_{timestamp.timestamp()}"
    # 存入
    collection.upsert(
        ids=[doc_id],
        embeddings=[embedding],
        metadatas=[metadata],
        documents=[content]
    )
    print(f"[向量库] 已存入：{content[:30]}...")

def search_similar_memories(user_id, query, top_k=5):
    """根据用户输入，从向量库中检索最相似的几条历史对话"""
    # 将用户的问题转成向量
    query_embedding = model.encode(query).tolist()
    # 查询
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"user_id": user_id}
    )
    # 解析结果
    similar = []
    if results['documents'] and results['documents'][0]:
        for i, doc in enumerate(results['documents'][0]):
            # 距离越小越相似，转换为相似度分数（0~1之间）
            score = 1 - results['distances'][0][i]
            similar.append((doc, score))
    return similar