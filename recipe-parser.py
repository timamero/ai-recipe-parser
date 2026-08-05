import os
import sys
import base64
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import List

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ["OPEN_API_PYTHON_RECIPE_KEY"])


# Define recipe structure
class Ingredient(BaseModel):
    name: str = Field(
        description="The name of the ingredient, e.g., 'all-purpose flour"
    )
    amount: str = Field(
        description="The quantity and unit, e.g., '2 cups', '1 tbsp', 'to taste'"
    )


class RecipeData(BaseModel):
    title: str = Field(description="The name of the recipe")
    prep_time: str = Field(description="Preparation time, e.g. '15 min'")
    cook_time: str = Field(description="Cooking time, e.g., '30 min")
    servings: int = Field(description="Number of servings the recipe makes")
    ingredients: List[Ingredient]
    instructions: List[str] = Field(
        description="Step-by-step cooking instructions in order"
    )
    estimated_calories: str = Field(
        description="Estimated number of calories per serving. Might be referred "
        "to as 'cal', 'total cal', 'energy' or other related. If not provided make "
        "an estimate based on ingredients and servings and specify if it "
        "is an estimate."
    )


# Get base64 string of image
def encode_image(image_path):
    """Encode an image in base64 characters"""
    with open(image_path, "rb") as imagefile:
        return base64.b64encode(imagefile.read()).decode("utf-8")


file_image_arg = sys.argv[1] if len(sys.argv) > 1 else None

base_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_dir, file_image_arg)
base64_image = encode_image(image_path)

prompt = """
    Extract the ingredients and steps from this recipe image into the requested JSON
    format. If the steps are missing, then infer from ingredients what the steps should
    be based on recipes with similar ingredients. If there is not title is missing, then
    infer from the ingredients what the title should be. If the cook time, prep time,
    or calories are missing, make an estimate and make it clear that time is an
    estimate.
"""

print("Analyzing recipe screenshot with gpt-4o-mini...")

# Call OpenAI API
response = client.responses.parse(
    model="gpt-4o-mini",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        }
    ],
    text_format=RecipeData,
)

parsed_recipe: RecipeData = response.output_parsed

# Export to Mardown
markdown_content = f"""# {parsed_recipe.title}

**Prep Time**: {parsed_recipe.prep_time}

**Cook Time**: {parsed_recipe.cook_time}

**Servings**: {parsed_recipe.servings}

**Estimated Calories**: {parsed_recipe.estimated_calories}

---

## Ingredients

"""

for ing in parsed_recipe.ingredients:
    markdown_content += f"- [ ] **{ing.amount}** {ing.name}\n"

markdown_content += "\n## Instructions\n"

for i, ins in enumerate(parsed_recipe.instructions):
    markdown_content += f"{i}. {ins}\n"

filename = f"{parsed_recipe.title.lower().replace(' ', '_')}.md"

with open(filename, "w", encoding="utf-8") as file:
    file.write(markdown_content)

print(f"Success! Saved recipe to : {filename}")
