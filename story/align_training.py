from langchain_core.messages import HumanMessage, SystemMessage
from langchain.tools import BaseTool

from util import add_meta, id_next, save_list_to_files, split_string_by_numbered_dots

trainings = [
    {
        "text": """
1. Выберете персонажа из истории, который будет озвучивать ваши мысли и чувства.
2. Какие неприятные чувства, которые уводят вас от ваших целей, вы часто испытываете? Проговорите их, если нужно запишите.[next]
3. Произнесите свою мысль 10 раз смешным мультяшным голосом.[next]
4. Произнесите свою мысль 5 раз очень МЕДЛЕННО, а потом БЫСТРО.[next]
5. Ваши мысли чувствуют себя теперь смешно или глупо?[any]
6. Потеряли ли они немного свою тяжесть?[any]
7. Произнося эти мысли по-другому, почувствовали ли вы себя немного лучше?[any]
8. Какой простой способ сделать ваши мысли смешными вы знаете?[any]
        """,
        "change": """
Все вопросы и последоватьность должны остаться неизменными. Приведи пример персонажа согласно истории,
обязательно приведём пример высказывания персонажа согласно истории забавным голосом. Но оставь выбор персонажа за ребёнком, не используй других названий и примеров, кроме тех что в истории.
        """,
        "meta": {"1":"[next]", "2":"[next]", "3":"[next]", "4":"[any]", "5":"[any]", "6":"[any]", "7":"[any]"}
     },
{
        "text": """
1. Выберете персонажа из истории, который будет озвучивать ваши мысли и чувства.
2. Какие неприятные чувства, которые уводят вас от ваших целей, вы часто испытываете? Проговорите их, если нужно запишите.[next]
3. Произнесите свою мысль 10 раз смешным мультяшным голосом.[next]
4. Произнесите свою мысль 5 раз очень МЕДЛЕННО, а потом БЫСТРО.[next]
5. Ваши мысли чувствуют себя теперь смешно или глупо?[any]
6. Потеряли ли они немного свою тяжесть?[any]
7. Произнося эти мысли по-другому, почувствовали ли вы себя немного лучше?[any]
8. Какой простой способ сделать ваши мысли смешными вы знаете?[any]
        """,
        "change": """
Все вопросы и последоватьность должны остаться неизменными. Приведи пример персонажа согласно истории,
обязательно приведём пример высказывания персонажа согласно истории забавным голосом. Но оставь выбор персонажа за ребёнком, не используй других названий и примеров, кроме тех что в истории.
        """,
        "meta": {"1":"[next]", "2":"[next]", "3":"[next]", "4":"[any]", "5":"[any]", "6":"[any]", "7":"[any]"}
     },
{
        "text": """
1. Выберете персонажа из истории, который будет озвучивать ваши мысли и чувства.
2. Какие неприятные чувства, которые уводят вас от ваших целей, вы часто испытываете? Проговорите их, если нужно запишите.[next]
3. Произнесите свою мысль 10 раз смешным мультяшным голосом.[next]
4. Произнесите свою мысль 5 раз очень МЕДЛЕННО, а потом БЫСТРО.[next]
5. Ваши мысли чувствуют себя теперь смешно или глупо?[any]
6. Потеряли ли они немного свою тяжесть?[any]
7. Произнося эти мысли по-другому, почувствовали ли вы себя немного лучше?[any]
8. Какой простой способ сделать ваши мысли смешными вы знаете?[any]
        """,
        "change": """
Все вопросы и последоватьность должны остаться неизменными. Приведи пример персонажа согласно истории,
обязательно приведём пример высказывания персонажа согласно истории забавным голосом. Но оставь выбор персонажа за ребёнком, не используй других названий и примеров, кроме тех что в истории.
        """,
        "meta": {"1":"[next]", "2":"[next]", "3":"[next]", "4":"[any]", "5":"[any]", "6":"[any]", "7":"[any]"}
     },
{
        "text": """
1. Выберете персонажа из истории, который будет озвучивать ваши мысли и чувства.
2. Какие неприятные чувства, которые уводят вас от ваших целей, вы часто испытываете? Проговорите их, если нужно запишите.[next]
3. Произнесите свою мысль 10 раз смешным мультяшным голосом.[next]
4. Произнесите свою мысль 5 раз очень МЕДЛЕННО, а потом БЫСТРО.[next]
5. Ваши мысли чувствуют себя теперь смешно или глупо?[any]
6. Потеряли ли они немного свою тяжесть?[any]
7. Произнося эти мысли по-другому, почувствовали ли вы себя немного лучше?[any]
8. Какой простой способ сделать ваши мысли смешными вы знаете?[any]
        """,
        "change": """
Все вопросы и последоватьность должны остаться неизменными. Приведи пример персонажа согласно истории,
обязательно приведём пример высказывания персонажа согласно истории забавным голосом. Но оставь выбор персонажа за ребёнком, не используй других названий и примеров, кроме тех что в истории.
        """,
        "meta": {"1":"[next]", "2":"[next]", "3":"[next]", "4":"[any]", "5":"[any]", "6":"[any]", "7":"[any]"}
     }
]

align_request = """
Упражнение:
[текст упражнения]

Инструкция по изменению упражнения:
[что можно менять]

Предыдущая часть истории:
[предыдущая часть]

Последующая часть истории:
[последующая часть]

Текст упражнения адаптированного согласно истории:
"""

align_messages = [SystemMessage(content="""
Вы дружелюбный и отзывчивый помощник, создающий творческий контент для детей с расстройством аутистического спектра. Вам будет предоставлен отрывок из истории, упражнение и дополнительная информация об интересах ребенка и целях упражнения.
Инструкции:
  История будет дана в двух частях, предыдущей и последующей, предыдущую ребёнок уже знает последующую еще нет.
  Не стоит раскрывать факты из последующей части, упражненеи только не длолжно противоречить последующей части истории.
  Используйте историю и упражнение, чтобы создать веселый и увлекательный опыт для ребенка с расстройством аутистического спектра.
  Сохраняйте последовательность персонажей, обстановки и сюжета на протяжении всей истории и упражнения.
  Обеспечьте при этом удовольствие и понимание ребенка.
  Используйте простой язык и четкие инструкции, избегая сложных предложений и ненужного жаргона.
  История уже включает интересы ребёнка, чтобы сделать опыт более понятным и мотивирующим.
  После упражнения будет дана инструкция какие части можно менять в упражнении. Все остальные нужно оставить как есть.
Твоя цель состоит в том, чтобы создать целостный и приятный опыт, который поможет ребенку с РАС развить конкретные навыки или поведение, одновременно задействуя его воображение и интерес через повествование.
""")]

def verify_text_is_training(text_to_check):
  global llm
  verify_messages = [SystemMessage(content="Тебе нужно проверить яляется ли текст упражнением для ребёнка. Если текст является выведи в ответ 1, иначе выведи в ответ 0.")]
  verify_messages.append(HumanMessage(content=f"Текст для проверки: {text_to_check} Ответ:"))
  res = llm(verify_messages)
  print(f"Результат проверки {res.content}")
  return res.content == '1'


# Выбирает упражнение и подстраивает под историю
class AlignTrainingTool(BaseTool):
    name = "align_trining"
    description = """Подготовка упражнения.
    Вызывается только после проверки качетсва истории.
    Примеры:
    Нужно подстороить упраженения под историю полсе её провери. (история проверена)"""

    def _run(
        self,
        run_manager=None,
    ) -> str:
        global story_parts, align_request, align_messages, trainings

        strings_to_save = []
        this_id, next_id = id_next()
        parts_amount = len(story_parts) - 1
        for idx in range(parts_amount):
          print(f"!!! готовлю упражнения: {idx}")
          request_text = align_request.replace("[предыдущая часть]", story_parts[idx])
          request_text = request_text.replace("[текст упражнения]", trainings[idx]["text"])
          request_text = request_text.replace("[что можно менять]", trainings[idx]["change"])
          request_text = request_text.replace("[последующая часть]", story_parts[idx +1])
          messages = align_messages
          messages.append(HumanMessage(content=request_text))
          res = llm(messages)
          aligned_training = res.content
          if not verify_text_is_training(aligned_training):
            print(f"!!! упражнение НЕ прошло проверку {idx}: {aligned_training}")
            return "Упражнения отменены. Нужно создвать заново историю запустить функцию create_story"
          print(f"!!! упражнение {idx}: {aligned_training}")
          strings_to_save.append(story_parts[idx])
          strings_to_save += add_meta(split_string_by_numbered_dots(aligned_training),trainings[idx]["meta"])
        strings_to_save.append(story_parts[-1])
        save_list_to_files(strings_to_save)
        return "Упражнения подготовлены."