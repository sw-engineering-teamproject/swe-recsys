import asyncio
from langchain_community.vectorstores import FAISS
import csv
class Document:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata

    def __str__(self):
        metadata_str = ', '.join([f'{key}: {value}' for key, value in self.metadata.items()])
        return f"Document(\n    page_content='{self.page_content}', \n    metadata={{\n        {metadata_str}\n    }}\n)"

async def build_faiss_cpu_db():
    reader = csv.reader(open('issue.csv', 'r', encoding='utf-8'))
    Documents = []

    for idx, row in enumerate(reader):
        if idx == 0:
            continue
        page_content = row[0] + " " + row[1]
        metadata = {'assignee_id': row[3], 'fixer_id': row[4]}
        Documents.append(Document(page_content, metadata))

    from langchain_text_splitters import CharacterTextSplitter

    text_splitter = CharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=0,
        separator="\n"
    )
    docs = text_splitter.split_documents(Documents)

    from langchain_community.embeddings import HuggingFaceEmbeddings

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2", encode_kwargs={'normalize_embeddings': True}
    )

    db = await FAISS.afrom_documents(docs, embeddings)

    DB_INDEX = "SWE_ASYNC_DB_INDEX"
    db.save_local(DB_INDEX)

if __name__ == '__main__':
    asyncio.run(build_faiss_cpu_db())