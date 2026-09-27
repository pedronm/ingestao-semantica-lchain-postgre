import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres import PGEngine, PGVectorStore

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
    #Quantos clientes temos em 2024?
    #Qual o faturamento da Empresa SuperTechIABrazil?
    TABLE_NAME = os.getenv("TABLE_NAME")
    CONNECTION_STRING = (f"postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}"
                         f"@{os.getenv("POSTGRES_URL")}/{os.getenv("POSTGRES_DB")}")
    load_dotenv()
    engine = PGEngine.from_connection_string(CONNECTION_STRING)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    model = ChatOpenAI(temperature=0.7, model_name="gpt-4.1-mini")

    store = PGVectorStore.create_sync(
        engine=engine,
        table_name=TABLE_NAME,
        embedding_service=embeddings,
    )

    docs_query = store.similarity_search_with_score(query=question, k=10)

    contexto = "\n\n".join(
        f"[score={score:.3f}] {document.page_content}"
        for document, score in docs_query
    )

    prompt = PromptTemplate.from_template(
        PROMPT_TEMPLATE,
    )

    chain = prompt | model | StrOutputParser()

    return chain.invoke({"pergunta":question,"contexto":contexto })