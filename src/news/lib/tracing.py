from pprint import pprint
from colorama import Back as B, Fore as F

def pre(*args, **kwargs):
    print("pre: ",args,kwargs)
    colors=kwargs['colors']
    name = kwargs['name']
    print(colors,flush=True)
    print(f"ENTERING {name}")

def post(*args, **kwargs):
    name = kwargs['name']
    print(f"LEAVING {name}")

    # print(F.RESET+B.RESET,flush=True)
    # exit()
    # print("After execution: Doing some cleanup work.")
    
def agent_tracer(before_func=None, after_func=None, **kwargs):
    print("agent_tracer: ",kwargs)
    def decorator(target_func):
        def wrapper(*args, **kwargs):
            if before_func:
                before_func(*args, **kwargs)
            result = target_func(*args, **kwargs)
            if after_func:
                after_func(*args, **kwargs)
            return result
        return wrapper
    return decorator    
    
    
def task_tracer(before_func=None, after_func=None, **kwargs):
    print("task_tracer: ",kwargs)
    def decorator(target_func):
        def wrapper(*args, **kwargs):
            if before_func:
                before_func(*args, **kwargs)
            result = target_func(*args, **kwargs)
            if after_func:
                after_func(*args, **kwargs)
            return result
        return wrapper
    return decorator    
    
    
    
    
    
    
    
    
def researcher_tracer(before_func=None, after_func=None, **kwargs):
    # print("tracing: ",kwargs)
    def decorator(target_func):
        def wrapper(*args, **kwargs):
            if before_func:
                before_func(*args, **kwargs)
            result = target_func(*args, **kwargs)
            if after_func:
                after_func(*args, **kwargs)
            return result
        return wrapper
    return decorator

def reporting_analyst_tracer(before_func=None, after_func=None, **kwargs):
    # print("tracing: ",kwargs)
    def decorator(target_func):
        def wrapper(*args, **kwargs):
            if before_func:
                before_func(*args, **kwargs)
            result = target_func(*args, **kwargs)
            if after_func:
                after_func(*args, **kwargs)
            return result
        return wrapper
    return decorator

def research_task_tracer(before_func=None, after_func=None, **kwargs):
    # print("tracing: ",kwargs)
    def decorator(target_func):
        def wrapper(*args, **kwargs):
            if before_func:
                before_func(*args, **kwargs)
            result = target_func(*args, **kwargs)
            if after_func:
                after_func(*args, **kwargs)
            return result
        return wrapper
    return decorator


def reporting_task_tracer(before_func=None, after_func=None, **kwargs):
    # print("tracing: ",kwargs)
    def decorator(target_func):
        def wrapper(*args, **kwargs):
            if before_func:
                before_func(*args, **kwargs)
            result = target_func(*args, **kwargs)
            if after_func:
                after_func(*args, **kwargs)
            return result
        return wrapper
    return decorator






def research_task_complete(task_result):
    name="research_task_complete"
    from colorama import Back as B, Fore as F
    print(F.LIGHTWHITE_EX+B.RED+name+F.RESET)
    print(B.CYAN,F.BLACK)
    pprint(task_result)
    print(B.RESET,F.WHITE)

def reporting_task_complete(task_result):
    name = "reporting_task_complete"
    from colorama import Back as B, Fore as F
    print(F.LIGHTWHITE_EX+B.RED+name+F.RESET)
    print(B.MAGENTA,F.BLACK)
    pprint(task_result)
    print(B.RESET,F.WHITE)

def researcher_complete(agent_result):
    name = "researcher_complete"
    from colorama import Back as B, Fore as F
    print(F.LIGHTWHITE_EX+B.RED+name+F.RESET)
    print(B.BLUE,F.WHITE)
    pprint(agent_result)
    print(B.RESET,F.WHITE)

def reporting_analyst_complete(agent_result):
    name = "reporting_analyst_complete"
    from colorama import Back as B, Fore as F
    print(F.LIGHTWHITE_EX+B.RED+name+F.RESET)
    print(B.GREEN,F.WHITE)
    pprint(agent_result)
    print(B.RESET,F.WHITE)