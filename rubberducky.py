import cmd
from constants import introduction, ducks
from model import Model
import subprocess
import os

from constants import bcolors

class RubberDuckShell(cmd.Cmd):
    intro = introduction
    prompt = "rubberduck>> "

    def __init__(self, model_name="meta-llama/Meta-Llama-3-8B"):
        super().__init__()
        self.last_traceback = None

        # token = os.getenv("HUGGINGFACE_TOKEN")
        # if not token:
        #     token = input("Enter your Huggingface token: ")
        # self.model = Model(token, model_name)

        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            api_key = input("Enter your GROQ API key: ")

        self.model = Model(api_key)

    def execute(self, args):
        try:
            args_list = args.split()
            script_path = args_list[0]
            script_args = args_list[1:]

            process = subprocess.Popen(['python', script_path] + script_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                print(f"{bcolors.OKCYAN}Script {script_path} failed with an error:{bcolors.ENDC}")
                print(stderr)
                self.last_traceback = stderr
                print(f"{bcolors.OKCYAN}Error captured. Run 'diagnose' command to diagnose the error.{bcolors.ENDC}")
            else:
                self.last_traceback = None
                print(f"Script {script_path} ran successfully with output:\n{stdout}")

        except Exception as e:
            print(f"Failed to run script {script_path}: {e}")

    def do_python(self, arg):
        "Run a Python script: python <script_path> [arguments]"
        self.execute(arg)

    def do_python3(self, arg):
        "Run a Python script: python3 <script_path> [arguments]"
        self.execute(arg)

    def do_diagnose(self, arg):
        "Diagnose the last error."
        if not self.last_traceback:
            print("No error log found. Please run a script that produces an error first.")
        else:
            diagnosis = self.model.inference(self.last_traceback)

            print(diagnosis)

    def do_exit(self, arg):
        "Exit the RubberDuck shell."
        print("Exiting RubberDuck shell.")
        return True
    
    def do_help(self, arg):
        "Command line help."
        commands = [attr[3:] for attr in dir(self) if attr.startswith('do_')]
        print("Available commands:")
        for command in commands:
            func = getattr(self, 'do_' + command)
            print(f"    {command}: {func.__doc__}")
    
    def do_quack(self, arg):
        "feed the ducks"
        print(ducks)

    def default(self, line):
        "Default handler for unrecognized commands."
        try:
            output = subprocess.check_output(line, shell=True, stderr=subprocess.STDOUT, text=True)
            print(output)
        except subprocess.CalledProcessError as e:
            print(e.output)

if __name__ == '__main__':
    RubberDuckShell().cmdloop()
