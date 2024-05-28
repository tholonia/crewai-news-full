# Python imports
import os
from pprint import pprint
from logging import log, basicConfig

basicConfig(level="INFO")

# Crew/Langchain imports
from crewai import Agent, Crew, Process, Task
from crewai_tools import tool
from crewai.project import (
    CrewBase,
    agent,
    crew,
    task,

)
# from crewai_tools import (
#     DirectoryReadTool,
#     FileReadTool,
#     WebsiteSearchTool,
# )

# Project imports
from src.news.lib.utils import is_verbose
from src.news.lib.utils import gget,gput
from crewai_tools import Tool

# gput("searcher","DDG") #override the input... for testing

search_name = "Search"
search_desc = "useful for when you need to answer questions about current events"

if gget('searcher') == "EXA":
    print(f"Using Search API: EXA")
    from src.news.lib.exa_search_tool import ExaSearchToolFull
    search_tool = Tool(name=search_name, description=search_desc, func=ExaSearchToolFull._exa().search)

if gget('searcher') == "DDG":  # still get ratelimit error
    from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
    search = DuckDuckGoSearchAPIWrapper()
    search.region="us-en"
    search.safesearch="off"
    search.backend="html" # backend: api, html, lite.
    # search.max_results=1 # even with only 1 query it fails with RateLimit :/
    search_tool = Tool(name=search_name, description=search_desc, func=search.run)

if gget('searcher') == "SER":
    print(f"Using Search API: SER")
    from langchain_community.utilities import GoogleSerperAPIWrapper
    search = GoogleSerperAPIWrapper(params={"engine": "bing","gl": "us","hl": "en"})
    search_tool = Tool(name=search_name, description=search_desc, func=search.run)

if gget('searcher') == "SAP": # defaults to SAP
    print(f"Using Search API: SAP")
    # REF: https://python.langchain.com/v0.1/docs/integrations/providers/serpapi/
    # REf: https://github.com/langchain-ai/langchain/issues/3485
    print(">>>",gget('SERPAPI_API_KEY'))
    from langchain_community.utilities import SerpAPIWrapper
    search = SerpAPIWrapper(params={"engine": "bing","gl": "us","hl": "en"})
    from crewai_tools import Tool
    search_tool = Tool(name=search_name, description=search_desc,func=search.run)

# Select which server to use
if gget('server') == "GOOGLE":
    # print("Sorry, GGL is currently not working")
    # exit()

    import google.generativeai as genai
    from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
    
    genai.configure(api_key='AIzaSyAMPuAw4CUoJ5yi1JAFktSasI4394rkfzc')
    
    llm_server = ChatGoogleGenerativeAI(
        # openai_api_base = gget("LIVE_API_BASE_URL"),
        model=gget("LIVE_MODEL_NAME"),
        verbose=is_verbose(gget("verbose")),
        temperature=0.1,
        google_api_key='AIzaSyAMPuAw4CUoJ5yi1JAFktSasI4394rkfzc'  # gget("LIVE_API_KEY"),
    )
else:
    from langchain_openai import ChatOpenAI as OpenAI

    llm_server = OpenAI(
        openai_api_base=gget("LIVE_API_BASE_URL"),
        openai_api_key=gget("LIVE_API_KEY"),
        model=gget("LIVE_MODEL_NAME"),
        temperature=0.0,
        verbose=is_verbose(gget("verbose")),
        max_tokens=4096,  # gpt-3.5 max_tokens = 4096
    )


@CrewBase
class NewsCrew():
    """News crew"""
    agents_config = "config/" + gget('agents_yaml')
    tasks_config = f"config/" + gget('tasks_yaml')

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=is_verbose(gget("verbose")),
            memory=bool(int(gget("memory"))),
            allow_delegation=bool(int(gget("delegation"))),
            llm=llm_server,
            tools= [
                # docs_tool,
                # file_tool,
                # search_tool,
                # web_rag_tool,
            ]
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=is_verbose(gget("verbose")),
            memory=bool(int(gget("memory"))),
            allow_delegation=bool(int(gget("delegation"))),
            llm=llm_server
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.researcher(),
        )

    @task
    def reporting_task(self) -> Task:
        # output_file = f"reports/{gget('COUNTER')}-{gget('server')}_{gget('LIVE_MODEL_NAME')}_{gget('topic')[:10].replace(' ','-')}.md"
        output_file = "reports/report" + gget("COUNTER") + "-" + gget('server') + "_" + gget(
            "LIVE_MODEL_NAME") + "_" + gget('topic')[:10].replace(" ", "-") + ".md"
        return Task(
            config=self.tasks_config['reporting_task'],
            agent=self.reporting_analyst(),
            output_file=output_file,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the News crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=bool(int(gget("verbose"))),
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
