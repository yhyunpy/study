# %%
import os
from datetime import datetime

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    FewShotPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv("local.env")

openai_api_key = os.getenv("OPENAI_API_KEY")


# %% 1. 프롬프트 템플릿

prompt_template = PromptTemplate.from_template(
    "안녕하세요, 제 이름은 {name}이고, 나이는 {age}살입니다."
)

# 프롬프트 템플릿 간의 결합
combined_prompt = (
    prompt_template
    + PromptTemplate.from_template("\n\n아버지를 아버지라 부를 수 없습니다.")
    + "\n\n{language}로 번역해주세요."
)

llm = ChatOpenAI(model="gpt-4o-mini")
chain = combined_prompt | llm | StrOutputParser()
chain.invoke({"age": 30, "language": "영어", "name": "홍길동"})

# %% 2. 챗 프롬프트 템플릿

# 2-튜플 형태의 메시지 목록으로 프롬프트 생성
chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "이 시스템은 천문학 질문에 답변할 수 있습니다."),
        ("user", "{user_input}"),
    ]
)

chain = chat_prompt | llm | StrOutputParser()
chain.invoke({"user_input": "태양계에서 가장 큰 행성은 무엇인가요?"})

# MessagePromptTemplate 활용
# 시스템 메시지와 사용자 메시지 템플릿을 포함하는 챗 프롬프트

chat_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "이 시스템은 천문학 질문에 답변할 수 있습니다."
        ),
        HumanMessagePromptTemplate.from_template("{user_input}"),
    ]
)

messages = chat_prompt.format_messages(
    user_input="태양계에서 가장 큰 행성은 무엇인가요?"
)

chain = chat_prompt | llm | StrOutputParser()
chain.invoke({"user_input": "태양계에서 가장 큰 행성은 무엇인가요?"})

# %% 4. Few-shot 프롬프트
# Few-shot : 언어모델에 예시를 제공하는 것

# 예제 포맷터
example_prompt = PromptTemplate.from_template("질문: {question}\n{answer}")

# 예제 세트
examples = [
    {
        "question": "지구의 대기 중 가장 많은 비율을 차지하는 기체는 무엇인가요?",
        "answer": "지구 대기의 약 78%를 차지하는 질소입니다.",
    },
    {
        "question": "광합성에 필요한 주요 요소들은 무엇인가요?",
        "answer": "광합성에 필요한 주요 요소는 빛, 이산화탄소, 물입니다.",
    },
    {
        "question": "피타고라스 정리를 설명해주세요.",
        "answer": "피타고라스 정리는 직각삼각형에서 빗변의 제곱이 다른 두 변의 제곱의 합과 같다는 것입니다.",
    },
    {
        "question": "지구의 자전 주기는 얼마인가요?",
        "answer": "지구의 자전 주기는 약 24시간(정확히는 23시간 56분 4초)입니다.",
    },
    {
        "question": "DNA의 기본 구조를 간단히 설명해주세요.",
        "answer": "DNA는 두 개의 폴리뉴클레오티드 사슬이 이중 나선 구조를 이루고 있습니다.",
    },
    {
        "question": "원주율(π)의 정의는 무엇인가요?",
        "answer": "원주율(π)은 원의 지름에 대한 원의 둘레의 비율입니다.",
    },
]

# FewShotPromptTemplat 생성
prompt = FewShotPromptTemplate(
    examples=examples,  # 사용할 예제들
    example_prompt=example_prompt,  # 예제 포멧팅에 사용할 템플릿
    suffix="질문: {input}",  # 예제 뒤에 추가될 접미사
    input_variables=["input"],  # 입력 변수 지정
)

# 새로운 질문에 대한 프롬프트를 생성하고 출력
print(prompt.invoke({"input": "화성의 표면이 붉은 이유는 무엇인가요?"}).to_string())


# %%
# 예제 선택기 사용하기

# SemanticSimilarityExampleSelector를 초기화
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,  # 사용할 예제들
    HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-nli"),  # 임베딩 모델
    Chroma,  # 벡터 저장소
    k=1,  # 선택할 예제 수
)

# 새로운 질문에 대해 가장 유사한 예제를 선택
question = "화성의 표면이 붉은 이유는 무엇인가요?"
selected_examples = example_selector.select_examples({"question": question})
print(f"입력과 가장 유사한 예제: {question}")
print(selected_examples)

# %% 채팅 모델에서 Few-shot 예제 사용하기

# 고정 예제 사용하기

# 예제 정의
examples = [
    {
        "input": "지구의 대기 중 가장 많은 비율을 차지하는 기체는 무엇인가요?",
        "output": "질소입니다.",
    },
    {
        "input": "광합성에 필요한 주요 요소들은 무엇인가요?",
        "output": "빛, 이산화탄소, 물입니다.",
    },
]

# 예제 프롬프트 템플릿 정의
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)

# Few-shot 프롬프트 템플릿 생성
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

# 최종 프롬프트 템플릿 생성
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 과학과 수학에 대해 잘 아는 교육자입니다."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
chain = final_prompt | model

# 모델에 질문하기
result = chain.invoke({"input": "지구의 자전 주기는 얼마인가요?"})
print(result.content)

# %%

# 동적 Few-shot 프롬프팅

# 더 많은 예제 추가
examples = [
    {
        "input": "지구의 대기 중 가장 많은 비율을 차지하는 기체는 무엇인가요?",
        "output": "질소입니다.",
    },
    {
        "input": "광합성에 필요한 주요 요소들은 무엇인가요?",
        "output": "빛, 이산화탄소, 물입니다.",
    },
    {
        "input": "피타고라스 정리를 설명해주세요.",
        "output": "직각삼각형에서 빗변의 제곱은 다른 두 변의 제곱의 합과 같습니다.",
    },
    {
        "input": "DNA의 기본 구조를 간단히 설명해주세요.",
        "output": "DNA는 이중 나선 구조를 가진 핵산입니다.",
    },
    {
        "input": "원주율(π)의 정의는 무엇인가요?",
        "output": "원의 둘레와 지름의 비율입니다.",
    },
]

# 벡터 저장소 생성
to_vectorize = [" ".join(example.values()) for example in examples]
embeddings = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-nli")
vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples)

# 예제 선택기 생성
example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=2,
)

# Few-shot 프롬프트 템플릿 생성
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_selector=example_selector,
    example_prompt=ChatPromptTemplate.from_messages(
        [("human", "{input}"), ("ai", "{output}")]
    ),
)

# 최종 프롬프트 템플릿 생성
final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 과학과 수학에 대해 잘 아는 교육자입니다."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

# 모델과 체인 생성
chain = final_prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

# 모델에 질문하기
result = chain.invoke("태양계에서 가장 큰 행성은 무엇인가요?")
print(result.content)

# %% 5. Partial Prompt
# 프롬프트 템플릿 부분 포맷팅하기

# 문자열을 사용한 부분 포맷팅

# 기본 프롬프트 템플릿 정의
prompt = PromptTemplate.from_template(
    "지구의 {layer}에서 가장 흔한 원소는 {element}입니다."
)

# 'layer' 변수에 '지각' 값을 미리 지정하여 부분 포맷팅
partial_prompt = prompt.partial(layer="지각")

# 나머지 'element' 변수만 입력하여 완전한 문장 생성
print(partial_prompt.format(element="산소"))

# 프롬프트 초기화 시 부분 변수 지정
prompt = PromptTemplate(
    template="지구의 {layer}에서 가장 흔한 원소는 {element}입니다.",
    input_variables=["element"],  # 사용자 입력이 필요한 변수
    partial_variables={"layer": "맨틀"},  # 미리 지정된 부분 변수
)

# 남은 'element' 변수만 입력하여 문장 생성
print(prompt.format(element="규소"))


# %%
# 함수를 사용한 부분 포맷팅


# 현재 계절을 반환하는 함수 정의
def get_current_season():
    month = datetime.now().month
    if 3 <= month <= 5:
        return "봄"
    elif 6 <= month <= 8:
        return "여름"
    elif 9 <= month <= 11:
        return "가을"
    else:
        return "겨울"


# 함수를 사용한 부분 변수가 있는 프롬프트 템플릿 정의
prompt = PromptTemplate(
    template="{season}에 일어나는 대표적인 지구과학 현상은 {phenomenon}입니다.",
    input_variables=["phenomenon"],  # 사용자 입력이 필요한 변수
    partial_variables={
        "season": get_current_season
    },  # 함수를 통해 동적으로 값을 생성하는 부분 변수
)

# 'phenomenon' 변수만 입력하여 현재 계절에 맞는 문장 생성
print(prompt.format(phenomenon="꽃가루 증가"))

# %%
