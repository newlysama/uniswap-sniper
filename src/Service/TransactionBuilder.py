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
    def buildCheckScamBundle(info: Info, pair: Pair, tx: dict) -> list :
        # Extract needed infos
        w3 = info.w3
        phantom = info.phantom
        token = pair.token
        sniperAddress = w3.to_checksum_address(info.sniper.address)

        logger.debug("Building checkScam transaction...")
        try:
            checkScamTx = phantom.contract.functions.checkScam(token.address).build_transaction({
                "from": sniperAddress,
                "nonce": w3.eth.get_transaction_count(sniperAddress),
                "gas": 300000,
                "gasPrice": w3.eth.gas_price
            });

        except Exception as e:
            raise Exception(f"could not build transaction : {str(e)}")
        logger.debug("TRANSACTION BUILT")

        body1 = {

        }

        # Check scam body
        body2 = {
            "chainId": 1,
            "from": str(sniperAddress),
            "to": str(phantom.address),
            "value": "0x0",
            "data": checkScamTx['data'],
            "gasLimit": 500000,
            "stateOverrides": {
                str(phantom.address): {
                    "balance": "100000000000000000000"  # 10 ETH
                }
            }
        }

        logger.debug("BUNDLE BUILT")

        return [body1, body2]
