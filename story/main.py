from langchain.agents import (
    AgentExecutor,
    create_gigachat_functions_agent,
)

from langchain.agents.gigachat_functions_agent.base import (
    format_to_gigachat_function_messages,
)
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_community.chat_models import GigaChat
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from typing import Optional, Type

from align_training import AlignTrainingTool
from story_critic import StoryCriticTool
from styory_teller import StoryTellerTool

credentials=""
scope='GIGACHAT_API_CORP'
model="GigaChat-Pro-preview"

system = """Ты агент по составлению истории. Ты составляешь историю, проверяешь её и готовишь упражнения.
Если получено указание выполнить функцию из приведённых ниже, нужно её выполнить.

У тебя есть доступные функции:
Создаёт историю create_story
Проверяет и оценивает историю check_story
Подготавливает упражнения align_trining

Не пиши одно и тоже пользователю.
Не придумывай данные сам.
Создавать и оценивать историю, готовить упражнения можно только используя функции."""

llm = GigaChat(
    verify_ssl_certs=False,
    timeout=300,
    model=model,
    credentials=credentials,
    scope=scope
)

story = ""
age = ""
interest = ""
story_parts = []


def run():
    chat_history = [SystemMessage(content=system)]

    age = "14 лет"
    interest = "плавание и компьютерные игры"

    tools = [StoryTellerTool(), StoryCriticTool(), AlignTrainingTool()]
    agent = create_gigachat_functions_agent(llm, tools)

    # AgentExecutor создает среду, в которой будет работать агент
    agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=False, return_intermediate_steps=True
    )

    user_input = "Соствь историю"
    result = agent_executor.invoke({"chat_history": chat_history,"input": user_input,})
    user_input = ""
    print( f"Bot: {result['output']}")


if __name__ == "__main__":
    run()