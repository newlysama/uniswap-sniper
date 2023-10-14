from sys import argv

from src.Logging import Logger

debugMod = argv.__contains__("--debug")

if debugMod:
    Logger.buildDevLogger()
else:
    Logger.buildMainLogger()

logger = Logger.get_logger()