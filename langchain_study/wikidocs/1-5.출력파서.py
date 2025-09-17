# %%
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import (CommaSeparatedListOutputParser,
                                           JsonOutputParser)
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

load_dotenv("local.env")

openai_api_key = os.getenv("OPENAI_API_KEY")
# %% 1. CSV Parser

output_parser = CommaSeparatedListOutputParser()
format_instructions = output_parser.get_format_instructions()

print(format_instructions)

prompt = PromptTemplate(
    template="List five {subject}.\n{format_instructions}",
    input_variables=["subject"],
    partial_variables={"format_instructions": format_instructions},
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# output_parser를 적용한 경우
chain = prompt | llm | output_parser
chain.invoke({"subject": "popular Korean cusine"})

# %%
# output_parser를 적용하지 않은 경우
chain = prompt | llm
chain.invoke({"subject": "popular Korean cusine"})

# %% 2. JSON Parser


# 자료구조 정의 (pydantic)
class CusineRecipe(BaseModel):
    name: str = Field(description="name of a cusine")
    recipe: str = Field(description="recipe to cook the cusine")


# 출력 파서 정의
output_parser = JsonOutputParser(pydantic_object=CusineRecipe)

format_instructions = output_parser.get_format_instructions()

print(format_instructions)

# prompt 구성
prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": format_instructions},
)

print(prompt)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# output_parser를 적용한 경우
chain = prompt | llm | output_parser
chain.invoke({"query": "Let me know how to cook Bibimbap"})
# %%
# output_parser를 적용하지 않은 경우
chain = prompt | llm
chain.invoke({"query": "Let me know how to cook Bibimbap"})

# %%
