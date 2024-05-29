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

async def search_faiss_cpu_db(query, db, k=5):
    from langchain_community.embeddings import HuggingFaceEmbeddings

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2", encode_kwargs={'normalize_embeddings': True}
    )
    embedding_vector = await embeddings.aembed_query(query)
    docs_and_scores = await db.asimilarity_search_with_score(query, k=k)
    searched = []
    for doc, score in docs_and_scores:
        searched.append(doc.metadata['assignee_id'])
        searched.append(doc.metadata['fixer_id'])

    result = []
    cnt = 0
    for i in searched:
        if i not in result:
            result.append(i)
            cnt += 1
        if cnt == 3:
            break
    return result

async def add_faiss_cpu_db(query, assignee_id, fixer_id, db):
    page_content = query + " " + assignee_id
    metadata = {'assignee_id': assignee_id, 'fixer_id': fixer_id}
    document = Document(page_content, metadata)
    db.add_documents([document])