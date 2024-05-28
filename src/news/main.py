#!/usr/bin/env python

# Preload all environment variables before other imports
import dotenv
dotenv.load_dotenv(dotenv_path='/home/jw/src/crewai/news/.env', override=True)
# python pkgs
import sys
import getopt
import time
# project pkgs
from src.news.lib.utils import (
    gget,
    gput,
    update_live_env,
    new_project_name,
    getdates,
    showhelp,
    printstats,
)
from src.news.lib.setserver import set_server
from news.crew import NewsCrew
# 3rd party pkgs
from langsmith.wrappers import wrap_openai
from langsmith import traceable


# Initialize vars to defaults
start_date, end_date = getdates("100 years ago:today") or (0, 0)
gput('start_date', start_date)
gput('end_date', end_date)

project_name = new_project_name()
gput("LANGCHAIN_PROJECT", project_name)

searcher = gput("searcher","SER") # Defaults to Serper

# Parse command-line arguments provided
try:
    opts, args = getopt.getopt(sys.argv[1:], "ht:v:m:s:r:p:l:d:S:", 
                                 ["help","topic=","verbose=","memory=","server=",
                                  "daterange=","prefix=","llm=","delegation=","searcher="])
except getopt.GetoptError as e:
    print(str(e))
    showhelp()
    sys.exit(2)

# options = {
#     "-t": "--topic",
#     "-h": "--help",
#     "-m": "--memory",
#     "-d": "--delegation",
#     "-v": "--verbose",
#     "-l": "--llm",
#     "-r": "--daterange",
#     "-p": "--prefix",
#     "-s": "--server"
# }

for opt, arg in opts:
    if opt in ("-t", "--topic"):        gput("topic", arg)
    elif opt in ("-h", "--help"):       showhelp()
    elif opt in ("-m", "--memory"):     gput("memory", int(arg))
    elif opt in ("-d", "--delegation"): gput("delegation", int(arg))
    elif opt in ("-v", "--verbose"):    gput("verbose", int(arg))
    elif opt in ("-l", "--llm"):        gput("LIVE_MODEL_NAME", arg)
    elif opt in ("-S", "--searcher"):   gput("searcher", arg)
    
    elif opt in ("-r", "--daterange"):
        thesedates = getdates(arg)
        gput("start_date", thesedates[0])
        gput("end_date", thesedates[1])
        
    elif opt in ("-p", "--prefix"):
        arg = arg.replace("'","")
        gput("prefix", arg)
        agents_yaml = f"{arg}_agents.yaml"
        tasks_yaml = f"{arg}_tasks.yaml"

        gput("agents_yaml", agents_yaml)
        gput("tasks_yaml", tasks_yaml)
        
    elif opt in ("-s", "--server"):
        gput("server", set_server(arg)) 
        update_live_env("SERVER",arg)
        update_live_env("API_BASE_URL",arg)
        update_live_env("API_KEY",arg)
        update_live_env("MODEL_NAME",arg)

def run():
    """
    The `run` function prints statistics before and after kicking off a NewsCrew task with specified
    inputs and measures the runtime.
    """
    printstats("before")
    # Inputs will automatically interpolate any tasks and agents information    
    inputs = {
        'topic': gget("topic"), #'AI LLMs'
        'start_date': gget('start_date'),
        'end_date': gget('end_date'),
     } 
    start_timer = time.time()
    NewsCrew().crew().kickoff(inputs=inputs)
    gput("runtime", int(time.time() - start_timer))
    printstats("after")    
    
