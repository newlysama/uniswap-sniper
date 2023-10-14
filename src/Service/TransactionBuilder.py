# Library imports
import json

# Local imports
from src.Class import Info, Pair
from src.GlobalLogger import logger

class TransactionBuilder :
    def __new__(cls):
        return

    # Static attribute saving sniper address
    address = json.load(open("resources/accounts.json", 'r'))['sniper']['address']

    @staticmethod
    def buildCheckScamBundle(info: Info, pair: Pair, tx: dict):
        # Extract needed infos
        phantom = info.phantom
        token = pair.token

        logger.debug("Building checkScam transaction...")
        try:
            checkTokenTx = phantom.contract.functions.checkScam(token.address).build_transaction({});
        except Exception as e:
            raise Exception(f"could not build transaction : {str(e)}")
        logger.debug("TRANSACTION BUILT")

        bundle = {
            "chainId": 1,  # Mainnet id
            "stateOverrides": {
                "balanceOverrides": {
                    str(TransactionBuilder.address): "10000000000000000000"  # 10 ETH in Wei
                }
            },
            "transactions": [
                {
                    "from": tx['from'],
                    "to": tx['to'],
                    "data": tx['input'],
                    "gasLimit": tx['gas'],
                    "value": str(tx['value'])
                },
                {
                    "from": str(TransactionBuilder.address),
                    "to": str(phantom.address),
                    "data": checkTokenTx['input'],
                }
            ]
        }

        logger.debug("BUNDLE BUILT")

        return bundle
