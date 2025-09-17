# %%
import asyncio
import os

import nest_asyncio
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv("local.env")

openai_api_key = os.getenv("OPENAI_API_KEY")

# %% 1. 기본 LLM 체인

# 언어모델
llm = ChatOpenAI(model="gpt-4o-mini")

# 프롬프트
prompt = ChatPromptTemplate.from_template(
    "You are an expert in astronomy. Answer the question. <Question>: {input}"
)

output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# 체인 실행
chain.invoke({"input": "지구의 자전 주기는?"})

# %% 2. 멀티 체인
prompt1 = ChatPromptTemplate.from_template("translates {korean_word} to English.")
prompt2 = ChatPromptTemplate.from_template(
    "explain {english_word} using oxford dictionary to me in Korean."
)

llm = ChatOpenAI(model="gpt-4o-mini")

chain1 = prompt1 | llm | StrOutputParser()
chain2 = {"english_word": chain1} | prompt2 | llm | StrOutputParser()

chain2.invoke({"korean_word": "미래"})

# %% 3. LangChain의 "Runnable" 프로토콜

prompt = ChatPromptTemplate.from_template(
    "지구과학에서 {topic}에 대해 간단히 설명해주세요."
)
model = ChatOpenAI(model="gpt-4o-mini")
output_parser = StrOutputParser()
chain = prompt | model | output_parser

# invoke : 단일 입력을 처리
result = chain.invoke({"topic": "지구 자전"})
print("invoke 결과:", result)

# batch : 여러 입력을 한꺼번에 처리
topics = ["지구 공전", "화산 활동", "대륙 이동"]
results = chain.batch([{"topic": t} for t in topics])
for topic, result in zip(topics, results):
    print(f"{topic} 설명: {result[:50]}...")

# stream : 모델이 생성하는 즉시 화면에 실시간 출력
stream = chain.stream({"topic": "지진"})
print("stream 결과:")
for chunk in stream:
    print(chunk, end="", flush=True)
print()

nest_asyncio.apply()


# ainvoke : 비동기 메소드
async def run_async():
    result = await chain.ainvoke({"topic": "해류"})
    print("ainvoke 결과:", result[:50], "...")


asyncio.run(run_async())

# %%
