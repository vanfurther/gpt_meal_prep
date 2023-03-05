from datetime import date
import time

import openai

# TODO this should ideally be retrieved from a secrets manager
openai.api_key = "<YOUR-KEY-HERE>"

# System content used to guide ChatGPT
# https://platform.openai.com/docs/guides/chat
be_chatgpt = f"""You are ChatGPT, a large language model trained by OpenAI.
Remember your prior reponses and use them when answering new prompts, if relevant.
Answer as concisely as possible.
Current date: {date.today()}"""

use_markdown = "Format your responses in GitHub Flavored Markdown. If not possible, format in plain text."

helpful_system_content = [
    {"role": "system", "content": be_chatgpt},
    {"role": "system", "content": use_markdown},
]

# User content to prompt ChatGPT
ask_for_spices = """Build a collection of spices in retail packaging that can be used for outdoor cooking.
The size of this collection must fit within a 25 liter packing cube."""

ask_for_meal_plan = """Using only the spice collection you just created for seasonings, create a 7 day meal plan for camping, which includes 3 meals per day.
Assume you have a 45 liter refrigerator for cold storage, no freezer, and 45 liters of additional storage for things that do not need to be refrigerated.
If a meal will use seasonings from the collection, tell me which seasonings are used and how.
Do not provide the ingredient list, I will ask for that next.
Optimize for using a minimal amount of ingredients."""

ask_for_overall_ingredient_list = """Provide an overall shopping list of ingredients for this meal plan, with just enough quantities for 2 adults, a 5 year old child, and a 2 year old child.
Include ingredients for everything mentioned in the meal plan.
Do not include ingredients not mentioned in the meal plan.
Do not include ingredients already in the spice collection.
Pretend you are a database and keep track of the remaining ingredients as I use them in future prompts."""

ask_for_remaining_ingredients = (
    "Provide all remaining ingredients from my shopping list."
)


def build_and_call(system_content: list[str], user_content: str) -> str:
    completion_messages = system_content + [{"role": "user", "content": user_content}]
    print(user_content + "\n")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=completion_messages,
        top_p=0.1,
    )
    print(completion["choices"][0]["message"]["content"] + "\n")
    # Avoid exceeding the rate limit of 20/min
    time.sleep(5)


def build_recipes(system_content: list[str]):
    meals = ["breakfast", "lunch", "dinner"]
    for x in range(7):
        day = x + 1
        for meal in meals:
            ask_for_recipe = f"""Provide cooking recipe for day {day} - {meal}.
            Keep track of ingredients used and how much you have left based on the database you're keeping.
            If you no longer have enough of an ingredient, please say you cannot provide a recipe because of it.
            You can only cook on a skottle grill, which is a cast iron disc with a 15.75 inch diameter over an 8455 BTU gas burner.
            If you need an oven, you can use a 6 quart cast iron camp dutch oven, which is heated by campfire only."""
            build_and_call(system_content, ask_for_recipe)


build_and_call(helpful_system_content, ask_for_spices)
build_and_call(helpful_system_content, ask_for_meal_plan)
build_and_call(helpful_system_content, ask_for_overall_ingredient_list)
build_recipes(helpful_system_content)
build_and_call(helpful_system_content, ask_for_remaining_ingredients)
