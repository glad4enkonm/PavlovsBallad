from util import extract_number
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.tools import BaseTool


# Критик
class StoryCriticTool(BaseTool):
    name = "check_story"
    description = """Проверяет критически качество составления истории.
    Вызывается только после создания истории.
    Примеры:
    Нужно проверить критически качество составления истории. (история создана)"""

    common = ""

    def __init__(self, common):
        super().__init__()
        self.common = common

    def _run(
        self,
        run_manager=None,
    ) -> str:
        
        story = self.common["story"]
        print(f"!!! проверяю историю:{ story }")
        messages = [
          SystemMessage(
            content="""Вы являетесь высококвалифицированным литературным критиком, задача которого - оценивать качество коротких рассказов. Ваша работа - прочитать предоставленный рассказ и оценить его по шкале от 0 до 10, где 0 - худший возможный балл, а 10 - лучший.
              При оценке рассказа учитывайте следующие критерии:
              1. Оригинальность и креативность сюжета и персонажей
              2. Логическую связность и плавность повествования
              3. Качество письма, включая описательный язык и диалоги
              4. Эмоциональное воздействие и способность увлечь читателя
              5. Отсутствие повторяющихся или избыточных элементов
              После прочтения рассказа предоставьте численную оценку от 0 до 10 в следующем формате 'оценка истории [оценка]' """
          ),
          HumanMessage(content=f"Вот история для оценки: {story}")
        ]
        res = self.common["llm"](messages)
        evaluation_result = res.content
        print(f"!!! {evaluation_result}")
        evaluation_number = extract_number(evaluation_result)
        if evaluation_number >= 8:
          result = ("Качество истории проверено критически и оценено.", "Запусти подготовку упражнения align_trining")
        else:
          result = ("Качество истории проверено критически и оценено.", "Нужно создать историю - запустить функцию create_story")
        return result