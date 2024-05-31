from colorama import Back, Fore 
from pprint import pprint
import functools
from src.news.lib.utils import tryit

def pre(name, colors):
# def pre(args,kwargs):
    # print("-------------------------------------------------------------------------")
    # pprint(args)
    # pprint(kwargs)
    # print("=========================================================================")
    # print(Fore.LIGHTWHITE_EX + Back.RED + f"{colors}" + Fore.RESET)
    print(colors, flush=True,end="")
    print(f"ENTERING {name}", flush=True,end="")
    print(Fore.RESET+Back.RESET,flush=True,)

def post(name,colors):
    print(colors, flush=True,end="")
    print(f"LEAVING {name}", flush=True,end="")
    print(Fore.RESET+Back.RESET, flush=True,)
    
def agent_tracer(before_func=None, after_func=None, **kwargs):
    def decorator(target_func):
        def wrapper(*args, **kwargs):
            if before_func:
                before_func(*args, **kwargs)
            result = target_func(*args, **kwargs)
            if after_func:
                after_func()
            return result
        return wrapper
    return decorator

def task_tracer(before_func=None, after_func=None, **kwargs):

    def decorator(target_func):
        @functools.wraps(target_func)
        def wrapper(*args, **kwargs):
            if before_func:
                before_func(*args, **kwargs)
            result = target_func(*args, **kwargs)
            if after_func:
                after_func(*args, **kwargs)
            return result
        return wrapper
    return decorator
    
    
def on_task_completion(*args,**kwargs):
    print(Fore.BLACK+Back.GREEN)
    name = tryit(kwargs,"name","none")
    print(f"┌───────────────────────────────────────────────────────────────────────────────────────────────────┐")
    print(f"│  {name}")
    print(f"└───────────────────────────────────────────────────────────────────────────────────────────────────┘")
    print(f"args: |{args}|")
    print(f"type: |{type(args)}|")
    print("=--==-=-=--")
    print(f"kwargs: |{kwargs}|")
    # print(f"│  {task_result}")
    print(Fore.RESET+Back.RESET)

def on_agent_completion(agent_result, **kwargs):
    print(Fore.GREEN+Back.RED)
    print(f"┌───────────────────────────────────────────────────────────────────────────────────────────────────┐")
    print(f"│  {kwargs['name']}")
    print(f"└───────────────────────────────────────────────────────────────────────────────────────────────────┘")
    print(f"│  {agent_result}")
    print(Fore.RESET+Back.RESET)
