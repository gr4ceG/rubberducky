# from transformers import AutoTokenizer, AutoModelForCausalLM
# from huggingface_hub import login
# import torch

from groq import Groq
# import traceback
import re

from constants import bcolors

from functionextract import extract_function_code

class Model:
    def __init__(self, api_key, model_name="llama3-8b-8192"):
        self.client = Groq(
            api_key=api_key # os.environ.get("GROQ_API_KEY"),
        )
        self.model_name = model_name

    def extract_filename_and_function(self, traceback_line):
        # Regex pattern
        pattern = re.compile(r'  File "(?P<filename>[^"]+)", line \d+, in (?P<function>[^\n]+)')
        
        # Search for the pattern in the traceback line
        match = pattern.search(traceback_line)
        if match:
            filename = match.group('filename')
            function_name = match.group('function')
            return filename, function_name
        return None, None

    def extract_function_context(self, tb_str):
        tb_lines = tb_str.splitlines()
        tb_lines = [line for line in tb_lines if line.startswith('  File')]
        traceback_info = []

        filepaths = []
        functions = []
        
        for frame in tb_lines:
            # print(f"frame: {frame}")
            filename, function_name = self.extract_filename_and_function(frame)
            traceback_info.append((filename, function_name))
            # print(f"Filename: {filename}")
            # print(f"function name: {function_name}")

            try:
                function_code = extract_function_code(filename, function_name)
                if function_code is not None:
                    filepaths.append(filename)
                    functions.append(function_code)
            except Exception as exce:
                print(exec)
        
        return filepaths, functions

    def inference(self, traceback):
        filepaths, functions = self.extract_function_context(traceback)
        function_context = "\n".join(f"File: {filepath}, Function: {function}" for filepath, function in zip(filepaths, functions))

        prompt = f"""
            Below is the traceback for the error message I recieved. Can you help diagnose and fix the issue? 
            Remember to be specific, add the file and the line number you're referring to. Give possibles solutions. 
            Get straight to the point.

            Traceback:
            {traceback}

            Functions:
            {function_context}
        """

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model_name,
        )
        return bcolors.OKBLUE + chat_completion.choices[0].message.content + bcolors.ENDC
