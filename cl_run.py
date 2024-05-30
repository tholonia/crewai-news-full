#!/bin/env python

# import warnings


# # Suppress all warnings globally (this will affect your entire program)
# with warnings.catch_warnings():
#     # Ignore all warning types by default
#     warnings.filterwarnings("ignore")

    
#     try:
#         # Your code here that may raise warnings
#         pass  # Replace this line with actual code
#     except Exception as e:
#         print(f"An exception occurred: {str(e)}")



#     try:
import src.news.main as main    
main.run()
# except Exception as e:
#     print(f"{e}")
#     print(e.with_traceback)



"""
# Example of a straight commandline run that does not use 'poetry'.
# To run in poetry, replace `./cl_run.py` with `poetry run news`.

 clear
 
 
 
./cl_run.py \
    --topic "Bitcoin news" \
    --server OPENAI \
    --verbose 2 \
    --memory 0 \
    --delegation 0 \
    --llm gpt-3.5-turbo \
    --daterange "10 years ago:today" \
    --searcher SER \
    --prefix 'default' \ 
 
 
# ╔═════════════════════════════════════════════════════════════
# ║ SEARCH and LLM COST (3.5 cheapest in cash)
# ╚═════════════════════════════════════════════════════════════
 
./cl_run.py \
    --topic "Bitcoin news" \
    --server OPENAI \
    --verbose 2 \
    --memory 0 \
    --delegation 0 \
    --llm gpt-3.5-turbo \
    --daterange "10 years ago:today" \
    --searcher SER \
    --prefix 'default' \

./cl_run.py -t "author and writer Matt Abrahams" -s OLLAMA -v 2 -m 1 -d 1 -l dolphin-llama3 -r "10 years ago:today" -S SER -p 'authors'

# ╔═════════════════════════════════════════════════════════════
# ║ SEARCH COST ONLY (cost credits only)
# ╚═════════════════════════════════════════════════════════════


./cl_run.py \
    --topic "author and writer Matt Abrahams" \
    --server OLLAMA \
    --verbose 2 \
    --memory 1 \
    --delegation 1 \
    --llm dolphin-llama3 \
    --daterange "10 years ago:today" \
    --searcher SER \
    --prefix 'authors' 
    
# 100% FREE    
# ╔═════════════════════════════════════════════════════════════
# ║ # 100% FREE    
# ╚═════════════════════════════════════════════════════════════

./cl_run.py \
    --topic "Matt Abrahams, writer and author" \
    --server GOOGLE \
    --verbose 2 \
    --memory 1 \
    --delegation 1 \
    --llm gpt-3.5-turbo \
    --daterange "10 years ago:today" \
    --searcher EXA \
    --prefix 'authors'     
    
"""
