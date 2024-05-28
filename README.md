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

Changes made to the projest created by running:

```
crewai create news
```

Which creates a structure that is not only reccomended, but which will be a prereq when they roll out their API.

- While poetry is not mandatory, it makes life easier, especially when it comes to version dependency, which is a total nightmare using pip.  If you need to run crew outside of poetry, go ahead and install and run poetry first, the, then look in the `poetry.lock` file to get the packages and their versions to create a `requirements.txt` file.
- Moved all the global vars, like API keys and counters to environment variables.
- Added the `utils.py` which holds general utility functions.
- To get VSCode to not complain about missing packages, I created a conda environment (miniforge3 version) and installed the packages (see `requirements.txt`), then switched my Python interpreter to that version.  Perhaps there is a way to select a poetry venv, but I don't see how.
- To run from the command line outside of poetry, create a wrapper script in the projects root folder like this:

```python
#!/bin/env python
import src.news.main as main
main.run()
```

See `cl_run.py` which has CL exmaples as well.

Make it executable, then you can just type `./scriptname.py` from inside the project folder.  You must have all the packages installed and be in the venv.

One reason to have a non-poetry version running is because poetry hide error messages.  For example, if a key is missing, you'll get lots of lines of errors, but not the most imoitant line:

```sh
KeyError: 'OPENAI_API_BASE_URL'
```

which you do get outside of poetry.

- Added `lib` folder and put a search and model selector classed in which allows for easy switching between OpenAI, a local Ollama of a local LM-Server ().
- Added langsmith monitoring by project name.

```
from langsmith.wrappers import wrap_openai
from langsmith import traceable
```

which allows for remote tracking of the workflow on the site https://smith.langchain.com/.  So far, this is the best way to track workflow activity (that I have found).  More info at https://docs.smith.langchain.com/

- Added command line switches with  which allows for easier testing of various models, etc., Current supporting teh following

```
    -t, --topic
    -h, --help
    -m, --memory
    -d, --delegation
    -v, --verbose
    -l, --llm
    -S, --searcher
    -r, --daterange
    -p, --prefix
    -s, --server
    
Example:
	cl_run.py \
        --topic "Bitcoin news" \
        --server OPENAI \
        --verbose 2 \
        --memory 0 \
        --delegation 0 \
        --llm gpt-3.5-turbo \
        --daterange "10 years ago:today" \
        --searcher SER \
        --prefix 'default' \
```

- Added option to select various predefined agents and tasks (`--prefix`)





# TODO

- Still not clear where to put th .env file.
- 