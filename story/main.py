from langchain.agents import (
    AgentExecutor,
    create_gigachat_functions_agent,
)

from langchain_community.chat_models import GigaChat
from langchain_core.messages import SystemMessage


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


story = ""
age = ""
interest = ""
story_parts = []


def run(age = "14 лет", interest = "плавание и компьютерные игры"):
    
    for _ in range(3):
        try:
            llm = GigaChat(
                verify_ssl_certs=False,
                timeout=300,
                model=model,
                credentials=credentials,
                scope=scope
            )
    
            chat_history = [SystemMessage(content=system)]
            common = {"age":age, "interest": interest, "llm": llm, "story_parts" : [], "file_id_to_start_chain": ''}
            tools = [StoryTellerTool(common), StoryCriticTool(common), AlignTrainingTool(common)]
            agent = create_gigachat_functions_agent(llm, tools)

            # AgentExecutor создает среду, в которой будет работать агент
            agent_executor = AgentExecutor(
                agent=agent, tools=tools, verbose=False, return_intermediate_steps=True
            )

            user_input = "Соствь историю"
            result = agent_executor.invoke({"chat_history": chat_history,"input": user_input})    
            print( f"Bot: {result['output']}")
            if common["file_id_to_start_chain"] == "":
                raise Exception("Не получено значение диалога")
            return common["file_id_to_start_chain"]
        except Exception as e:
            print("Ошибка", e)
    return ""

if __name__ == "__main__":
    run()