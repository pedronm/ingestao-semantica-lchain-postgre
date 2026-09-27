import os
import asyncio

from langchain_postgres import PGEngine, PGVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from dotenv import load_dotenv

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
CONNECTION_STRING = (f"postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}"
                     f"@{os.getenv("POSTGRES_URL")}/{os.getenv("POSTGRES_DB")}")
TABLE_NAME = os.getenv("TABLE_NAME")

VECTOR_SIZE=1536
EMBBEDINGS=OpenAIEmbeddings(
    model="text-embedding-3-small",
)
ENGINE = PGEngine.from_connection_string(CONNECTION_STRING)


async def ingest_pdf():

    create_table()

    store = PGVectorStore.create_sync(
        engine=ENGINE,
        table_name=TABLE_NAME,
        embedding_service=EMBBEDINGS,

    )

    loader = PyPDFLoader(
        file_path=PDF_PATH,
        mode="single",
        pages_delimiter= ''
    )

    pages = loader.load()

    #print(pages[0].page_content)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
        is_separator_regex=False,
    )

    split_docs = text_splitter.split_documents(pages)
    pages = [doc.page_content for doc in split_docs]
    embeddings = EMBBEDINGS.embed_documents(pages)

    store.add_embeddings(text_splitter=text_splitter, documents=pages, texts=pages, embeddings=embeddings)

def create_table():
    ENGINE.init_vectorstore_table(
        table_name=TABLE_NAME,
        vector_size=VECTOR_SIZE,
    )

if __name__ == "__main__":
    asyncio.run(ingest_pdf())