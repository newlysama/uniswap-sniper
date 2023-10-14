# Library imports
from sys import argv

# Local imports
from src.Service import Loader
from src.GlobalLogger import logger
from src.Service.MempoolListener import MempoolListener

from src.Class import Token, Utils
import requests as requests
import json

class Program :
    def __init__(self) :
        logger.status("STARTING LOADING PROCESS")
        loader = Loader()
        try :
            self.info = loader.loadInfo()
        except Exception as e:
            logger.critical(f"Exception raised during loading process [{str(e)}]")
            exit(1)

        del loader
        print()


    def launchProgram(self):
        logger.status("STARTING LISTENING PROCESS")
        listener = MempoolListener(self.info)
        listener.listen()


####### LAUNCH PROGRAM #######

program = Program()
program.launchProgram()
