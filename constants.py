import random

class bcolors:
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

logo = bcolors.YELLOW + """
            _     _                  _            _          
           | |   | |                | |          | |         
 _ __ _   _| |__ | |__   ___ _ __ __| |_   _  ___| | ___   _ 
| '__| | | | '_ \| '_ \ / _ \ '__/ _` | | | |/ __| |/ / | | |
| |  | |_| | |_) | |_) |  __/ | | (_| | |_| | (__|   <| |_| |   
|_|   \__,_|_.__/|_.__/ \___|_|  \__,_|\__,_|\___|_|\_\\\\__, |    
                                                        __/ |
                                                        |___/ 
""" + bcolors.ENDC
commands = """
   _______________________________________________________________
 /                                                                 \\
|    Welcome to (talking) rubberducky. Type "help" for commands.    |
 \_________________________________________________________________/ 
                                            \\
"""
ducks = bcolors.BOLD + bcolors.YELLOW + """
                                            >(.)__ <(.)__ =(.)__
                                             (___/  (___/  (___/ 
""" + bcolors.ENDC

introduction = logo + "\n" + commands + "\n" + ducks

quack_bubble = """
                                      ____________
                                     /             \\
                                    |    quack.    |
                                     \____________/ 
                                            \\
"""

def random_duck():
    choice = random.randint(0, 2)
    beaks = ['>', '<', '=']
    duck1 = f"""
                                                {beaks[choice]}(.)__ 
                                                 (___/
    """

