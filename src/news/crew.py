# Python imports

# import warnings
# with warnings.catch_warnings():
#     warnings.filterwarnings("ignore",category=FutureWarning)
    
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
from colorama import Back as B, Fore as F
 
# Project imports
from src.news.lib.utils import gget, is_verbose, mkdir
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

# REF: https://python.langchain.com/v0.1/docs/integrations/providers/serpapi/
# REf: https://github.com/langchain-ai/langchain/issues/3485
if gget('search') == "SAP": # defaults to SAP
    print(f"Using Search API: SAP")
    print(">>>",gget('SERPAPI_API_KEY'))
    from langchain_community.utilities import SerpAPIWrapper
    search = SerpAPIWrapper(params={"engine": "bing","gl": "us","hl": "en"})
    from crewai_tools import Tool
    search_tool = Tool(name=search_name, description=search_desc,func=search.run)

# Select which server to use
if gget('server') == "GOOGLE":
    print("Sorry, GGL is currently not working")
    exit()
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



from langchain_openai import ChatOpenAI as OpenAI

llm_server = OpenAI(
    openai_api_base=gget("LIVE_API_BASE_URL"),
    openai_api_key=gget("LIVE_API_KEY"),
    model=gget("LIVE_MODEL_NAME"),
    temperature=0.0,
    verbose=is_verbose(gget("verbose")),
    max_tokens=4096,  # gpt-3.5 max_tokens = 4096
)

from crewai_tools import FileReadTool
file_read_tool = FileReadTool


# Create an outfile name root like output_file that looks like
# "rpt328-OLL-phi3_dtr_"

#output_file_basename = "reports/rpt" + gget("COUNTER") + "-" + gget('server') + "_" + gget("LIVE_MODEL_NAME") + "_" + gget('topic')[:10].replace(" ", "-") + ".md"


topic_stub=gget('topic')[:10].replace(" ", "-")
# report_dir = mkdir(f"reports")
# report_subdir = mkdir(f"reports/reports-{topic_stub}")
report_subdir = f"reports/reports-{topic_stub}-{gget('server')[:3]}-{gget('LIVE_MODEL_NAME')}"
# outbase = f"{report_subdir}{gget('server')[:3]}-{gget('LIVE_MODEL_NAME')}"
# print(outbase)
# exit()

# print(f"outbase: {outbase}")
# print(f"report_dir: {report_dir}")
# print(f"topic_stub: {topic_stub}")





from src.news.lib.tracing import (
    agent_tracer,
    task_tracer,
    on_task_completion,
    on_agent_completion,
    pre,
    post,
)


@CrewBase
class NewsCrew():
    """News crew"""
    agents_config = "config/" + gget('agents_yaml')
    tasks_config = f"config/" + gget('tasks_yaml')


    @agent
    @agent_tracer(
        before_func=pre(name="researcher",colors=F.RED+B.BLACK,), 
        after_func=post(name="researcher",colors=F.RED+B.BLACK,),
        )
    def researcher(self) -> Agent:
        print(("AGENT researcher"))
        stub = "A-researcher"
        return Agent(
            config=self.agents_config['researcher'],
            verbose=is_verbose(gget("verbose")),
            memory=bool(int(gget("memory"))),
            allow_delegation=bool(int(gget("delegation"))),
            llm=llm_server,
            tools= [
                file_read_tool,
                search_tool,
                # web_rag_tool,
            ],
            output_file=f"{report_subdir}/{gget('COUNTER')}-{stub}.md",
            # callback=on_agent_completion(name="XXXXXX"),
            
        )

    @agent
    @agent_tracer(before_func=pre(name="reporting_analyst", colors=F.GREEN+B.BLACK), after_func=post(name="reporting_analyst",colors=F.GREEN+B.BLACK,))
    def reporting_analyst(self) -> Agent:
        print(("AGENT reporting_analyst"))
        stub = "A-reporting_analyst"
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=is_verbose(gget("verbose")),
            memory=bool(int(gget("memory"))),
            allow_delegation=bool(int(gget("delegation"))),
            llm=llm_server,
            output_file=f"{report_subdir}/{gget('COUNTER')}-{stub}.md",
            tools= [
                file_read_tool,
                search_tool,
                # web_rag_tool,
            ],
            
            # callback=on_agent_completion,
            
        )

    @task
    @task_tracer(before_func=pre(name="research_task", colors=F.CYAN+B.BLACK), after_func=post(name="research_task",colors=F.CYAN+B.BLACK,))
    
    def research_task(self) -> Task:
        print(("TASK research_task"))        
        stub = "T-research_task"
        rs = Task(
            config=self.tasks_config['research_task'],
            agent=self.researcher(),
            output_file=f"{report_subdir}/{gget('COUNTER')}-{stub}.md",
            callback=on_task_completion(name="NAME"),
            tools= [
                file_read_tool,
                search_tool,
                # web_rag_tool,
            ],
        )
        """
        at this point, 'rs' is a tuple of tuples that hold the input parameters
        """        
        pprint(list(rs))
        # exit()
        return rs

    @task
    @task_tracer(before_func=pre(name="reporting_task", colors=F.MAGENTA+B.BLACK), after_func=post(name="reporting_task",colors=F.MAGENTA+B.BLACK,))
    
    def reporting_task(self) -> Task:
        print(("TASK reporting_task"))        
        stub = "T-reporting_task"
        rs = Task(
            config=self.tasks_config['reporting_task'],
            agent=self.reporting_analyst(),
            output_file=f"{report_subdir}/{gget('COUNTER')}-{stub}.md",
            callback=on_task_completion(name="AAAAAA"),
            tools= [
                file_read_tool,
                search_tool,
                # web_rag_tool,
            ],
            
        )
        return rs       

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
