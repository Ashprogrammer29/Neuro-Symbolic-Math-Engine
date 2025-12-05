#This error indicates you are running the script using the correct path
#but Python is failing to recognize the src directory as a valid package from which to import modules.

#When you execute python src/language_model.py, Python treats language_model.py as the top-level script.
#When that script tries to run from src.config import...,
# Python looks for a folder named src relative to its search path, which usually starts at the current working directory (offline_chatbot).


#You must add an empty file named __init__.py into your src directory
# to signal to Python that it should treat src as a package.

