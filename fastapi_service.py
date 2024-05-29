class Document:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata

async def load_faiss_cpu_db(db_index):
    from langchain_community.embeddings import HuggingFaceEmbeddings

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2", encode_kwargs={'normalize_embeddings': True}
    )
    from langchain_community.vectorstores import FAISS
    db = FAISS.load_local(db_index, embeddings, allow_dangerous_deserialization=True)
    return db
