from src.Class import Info, Pair
from src.GlobalLogger import logger
from src.Service.PairChecker import PairChecker

class PairProcessor :
    def __init__(self, info : Info, pair : Pair, tx : dict):
        self.info = info
        self.pair = pair
        self.tx = tx

    def processPair(self):
        # Extract needed data
        token = self.pair.token

        logger.info(f"Checking if {token.symbol} is a scam...")
        pairChecker = PairChecker(self.info, self.pair, self.tx)

        try :
            pairChecker.checkScam()
        except Exception as e:
            logger.error(f"Scam checking failed : {str(e)}")
            return