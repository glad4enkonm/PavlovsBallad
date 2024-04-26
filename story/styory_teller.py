from util import split_text_by_block
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.tools import BaseTool

# Сочинитель истории
class StoryTellerTool(BaseTool):
    name = "create_story"
    description = """Создаёт популярные и увлекательные детски истории.
    Возвращает историю состоящую из блоков.

    Примеры:
    Нужно создать историю"""
    common = ""

    def __init__(self, common):
        super().__init__()
        self.common = common        
    

    def _run(
        self,
        run_manager=None,
    ) -> str:
        age = self.common["age"]
        interest = self.common["interest"]
        print(f"!!! Создаю историю для возраста:{age} и интересов:{interest}")
        messages = [
          SystemMessage(
            content="""Ты автор популярных и увлекательных детских историй, читатели не могут оторваться от твоих произведений,каждый раз нужно придумывать новую историю. История должна состоять из 4 блоков по 500 слов, разделённых тектом Блок [номер].Выводи только текст истории и разделители блоков. Эта история будет использована для включения в неё терапевтических упражнений.Ребёнок аутист."""
          ),
          HumanMessage(content=f"Составь историю для ребёнка {age} лет, ребёнок увлекается {interest}.")
        ]
        res = self.common["llm"](messages)        
        self.common["story"] = res.content
        self.common["story_parts"] = split_text_by_block(self.common["story"])
        if len(self.common["story_parts"]) == 4:
          print("История готова")
          result = "Запусти функцию проверки истории check_story"
        else:
          print("История НЕ получилась")
          result = "Запусти функцию создания истории create_story"
        return result