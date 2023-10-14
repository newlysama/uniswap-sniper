import logging
import logging.config
import yaml
from src.Logging.CustomFormatter import CustomFormatter

def addLoggingLevel(levelName, levelNum, methodName=None):
    """
    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5
    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
       raise AttributeError('{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
       raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
       raise AttributeError('{} already defined in logger class'.format(methodName))

    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)

class Logger:
    _logger = None

    @staticmethod
    def buildMainLogger():
        with open('logs/logger_config.yaml', 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        Logger._logger = logging.getLogger('mainLogger')

    @staticmethod
    def buildDevLogger():
        with open('logs/logger_config.yaml', 'r') as f:
            config = yaml.safe_load(f.read())
            addLoggingLevel('STATUS', 35)
            addLoggingLevel('SUCCESS', 30)
            logging.config.dictConfig(config)

        logger = logging.getLogger('devLogger')
        for handler in logger.handlers:
            handler.setFormatter(CustomFormatter(
                '[%(asctime)s] - %(log_color)s%(levelname)s - %(message)s',
                    datefmt='%H:%M:%S',
            ))
        Logger._logger = logger

    @staticmethod
    def get_logger():
        return Logger._logger
