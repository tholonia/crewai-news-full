#!/usr/bin/env python
# import warnings
# with warnings.catch_warnings():
#     warnings.filterwarnings("ignore",category=FutureWarning)

# Preload all environment variables before other imports
import dotenv
dotenv.load_dotenv(dotenv_path='/home/jw/src/crewai/news/.env', override=True)
# python pkgs
import sys
import getopt
import time

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
# needs internet
# from langsmith.wrappers import wrap_openai
# from langsmith import traceable


# Initialize vars to defaults

start_date, end_date = getdates("100 years ago:today") or (0, 0)
gput('start_date', start_date)  # Defaults to 100 years ago
gput('end_date', end_date)  # Defaults to today
gput('searcher', 'OFF')  # Defaults to OFF
gput("LANGCHAIN_PROJECT", new_project_name())
gput("inputfile","None") # Defaults to Serper
gput("topic","None") # Defaults to Serper
gput("test","test") # Defaults to Serper


# Parse command-line arguments provided
try:
    opts, args = getopt.getopt(sys.argv[1:], "ht:v:m:s:r:p:l:d:S:i:", 
                                 ["help","topic=","verbose=","memory=","server=",
                                  "daterange=","prefix=","llm=","delegation=","searcher=","inputfile="])
except getopt.GetoptError as e:
    print(str(e))
    showhelp()
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-t", "--topic"):        gput("topic", arg)
    elif opt in ("-h", "--help"):       showhelp()
    elif opt in ("-m", "--memory"):     gput("memory", int(arg))
    elif opt in ("-d", "--delegation"): gput("delegation", int(arg))
    elif opt in ("-v", "--verbose"):    gput("verbose", int(arg))
    elif opt in ("-l", "--llm"):        gput("LIVE_MODEL_NAME", arg)
    elif opt in ("-S", "--searcher"):   gput("searcher", arg)
    elif opt in ("-i", "--inputfile"):  gput("inputfile", arg)
    
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
        
print(f">>> |{gget('inputfile')}| |{gget('topic')}|")

if gget("inputfile") != "None" and (gget("topic") == "None" or gget("topic") == ""): 
    gput("topic",gget("inputfile")) # Defaults to Serperinput  
    
    
print(gget("inputfile"),gget("topic"))    
# exit()

# these are loAded after we set all teh default vars so the loaded modules see the updated defaults
# project pkgs


from src.news.crew import NewsCrew



def run():
    """
    The `run` function prints statistics before and after kicking off a NewsCrew task with specified
    inputs and measures the runtime.
    """
    printstats("before")
    
    # exit()
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
    
