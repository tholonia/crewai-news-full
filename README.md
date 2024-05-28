The first section below is the original readme file from the official crew AI documentation, which successfully shows how to set up a simple crew. Below this section is Part II, which is my hands-on command-line experience installing this and getting it up and running, along with some other potentially useful notes.

# News Crew

Welcome to the News Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install Poetry:

```bash
pip install poetry
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and then install them:
```bash
poetry lock
```
```bash
poetry install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/news/config/agents.yaml` to define your agents
- Modify `src/news/config/tasks.yaml` to define your tasks
- Modify `src/news/crew.py` to add your own logic, tools and specific args
- Modify `src/news/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
poetry run news
```

This command initializes the news Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The news Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the News Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.



# Part II

|>>

While poetry is not mandatory, it makes life easier, especially when it comes to version dependency, which is a total nightmare using pip.  If you need to run crew outside of poetry, go ahead and install and run poetry first, the, then look in the `poetry.lock` file to get the packages and their versions to create a `requirements.txt` file.

|>>

I have added a `gvars.py`  file which is used to hold global variables across classes and modules.  Perhaps not a 'best practice' in coding, but very convenient and useful.  Also added the `utils.py` and `gutils.py`, which hold simple utility functions.  The `gutils.py` are utils that do NOT require the `gvars.py`, while `utils.py` does.  This is to avoid cyclical dependencies.

|>>

To get VSCode to not complain about missing packages, I created a conda environment (miniforge3 version) and installed the packages, then switched my Python interpreter to that version.  Perhaps there is a way to select a poetry venv, but I don't see how.

|>>

To run from the command line outside of poetry, create a wrapper script in the projects root folder like this:

```python
#!/bin/env python
import src.news.main as main
main.run()
```

Make it executable, then you can just type `./scriptname.py` from inside the project folder.  You must have all the packages installed and be in the venv.

One reason to have a non-poetry version running is because poetry hide error messages.  For example, if a key is missing, you'll get lots of lines of errors, but not the most imoitant line:

```sh
KeyError: 'OPENAI_API_BASE_URL'
```

which you do get outside of poetry.

|>>

Added `lib` folder and put a model selector class in `model_selector.py` which allows for the choosing between OpenAI, a local Ollama of a local LM-Server ().

Running the questions that are automatically installed, I get the following specs.  (Local machine is 4080Ti)

OpenAI/GPT4-turbo: 

- 178 seconds, made a nice full page report in MD with outlines

Ollama/phi3:

- 90 seconds, made report of a few sad sentences.

LMS/phi3 or Claude

- Crashes

|>>

Added 
```
from langsmith.wrappers import wrap_openai
from langsmith import traceable
```

which allows for remote tracking of the workflow on the site https://smith.langchain.com/.  So far, this is the best way to track workflow activity (that I have found).  More info at https://docs.smith.langchain.com/


|>>
Added command line switches with getopt() which allows for easier testing of varers flags and services.



"""
This is the system prompt I used to tweak my local LLM's... but they still don't work well enough :/

You are an AI language model designed to be a thorough and complete researcher. Your goal is to provide accurate, detailed, and well-researched information. When answering questions or providing information, follow these guidelines:
Accuracy: Ensure all facts are correct and verified from reliable sources.
Detail: Provide comprehensive answers, covering all relevant aspects of the topic.
Clarity: Use clear and precise language. Avoid ambiguity and ensure the reader can easily understand the information.
Citations: Where applicable, cite sources to back up your information.
Verification: Double-check facts and data for accuracy.
Clarification: Proactively ask for additional information if a query is ambiguous or lacking in detail.
Objectivity: Present information in an unbiased and neutral manner.
Relevance: Stay focused on the topic and avoid providing unnecessary or unrelated information.
Structure: Organize information logically, using headings, bullet points, and paragraphs to enhance readability.
"""
  


   pip install google-search-results