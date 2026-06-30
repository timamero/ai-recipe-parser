# AI Recipe Parser

An intelligent recipe extraction tool that uses OpenAI's GPT-4o-mini to parse recipe images and convert them into structured markdown documents.

## Features

- Extract recipes from images using AI vision
- Automatically structure recipes into markdown format
- Parse ingredients with quantities and units
- Extract or estimate prep and cook times
- Include estimated calorie information
- Generate step-by-step cooking instructions

## Tech Stack

- **Language**: Python
- **AI Model**: OpenAI GPT-4o-mini with structured output
- **Data Validation**: Pydantic
- **API Client**: OpenAI Python
- **Environment Management**: python-dotenv
- **Package Manager**: Poetry

## Installation

### Prerequisites

- Python 3.13 or higher
- OpenAI API key

### Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd python-ai-recipe
   ```

2. **Install dependencies using Poetry**

   ```bash
   poetry install
   ```

3. **Configure environment variables**

   Create a `.env` file in the project root and add your OpenAI API key:

   ```
   OPEN_API_PYTHON_RECIPE_KEY=your_api_key_here
   ```

## Usage

### Running the Parser

```bash
make run
```

Or directly with Poetry:

```bash
poetry run python recipe-parser.py
```

This will:

1. Process the image (`insta-recipe.jpg`)
2. Send it to GPT-4o-mini for analysis
3. Extract recipe data (ingredients, instructions, times, servings, calories)
4. Generate a markdown file with the structured recipe

### Output

The script generates a markdown file named after the recipe (e.g., `easy_beef_curry.md`), formatted with:

- Recipe title
- Prep and cook times
- Servings and estimated calories
- Ingredient list with checkboxes
- Numbered cooking instructions

## Example Output

See sample recipes:

- [easy_beef_curry.md](easy_beef_curry.md)
- [tiramisu.md](tiramisu.md)
