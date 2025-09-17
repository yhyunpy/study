# %%
import os

from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

load_dotenv("local.env")

openai_api_key = os.getenv("OPENAI_API_KEY")
# %%
# 기본 컴포넌트 설정
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "당신은 천문학 전문가입니다. 사용자와 친근한 대화를 나누며 천문학 질문에 답변해주세요.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

# 메모리 저장소 구성
store = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
chain = prompt | llm

# 메모리 기능을 가진 체인 생성
chain_with_history = RunnableWithMessageHistory(
    chain,  # 기본 체인
    get_session_history,  # 세션 히스토리를 가져오는 함수
    input_messages_key="question",  # 사용자 입력 키
    history_messages_key="history",  # 대화 기록 키
)

# 세션 아이디 설정
config = {"configurable": {"session_id": "astronomy_chat_1"}}

# 첫 번째 대화
response1 = chain_with_history.invoke(
    {"question": "안녕하세요, 저는 지구과학을 공부하는 학생입니다."}, config=config
)

# %%
# 두 번째 대화 - 컨텍스트 유지
response2 = chain_with_history.invoke(
    {"question": "태양계에서 가장 큰 행성은 무엇인가요?"}, config=config
)

# %%
# 세 번째 대화 - 참조 관계 이해
response3 = chain_with_history.invoke(
    {"question": "그 행성의 위성은 몇 개나 되나요?"}, config=config
)

# %%
