# %%
import os

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv("local.env")

openai_api_key = os.getenv("OPENAI_API_KEY")


# %% 1. 데이터 로드
# 위키피디아 정책과 지침
url = "https://ko.wikipedia.org/wiki/%EC%9C%84%ED%82%A4%EB%B0%B1%EA%B3%BC:%EC%A0%95%EC%B1%85%EA%B3%BC_%EC%A7%80%EC%B9%A8"
loader = WebBaseLoader(url)

# 웹페이지 텍스트 -> Documents
docs = loader.load()

print(len(docs))
# %% 2. 텍스트 분할

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

print(len(splits))

# %% 3. 인덱싱

# embedding 모델로 텍스트를 벡터로 변환, 이를 Chroma 벡터 저장소에 저장
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-nli"),
)

# %% 4. 검색

# Prompt
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Rretriever
#  Chroma 벡터 스토어를 검색기로 사용하여 사용자의 질문과 관련된 문서를 검색
retriever = vectorstore.as_retriever()


# %% 5. 생성
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# Chain 실행
rag_chain.invoke("격하 과정에 대해서 설명해주세요.")

# %%
