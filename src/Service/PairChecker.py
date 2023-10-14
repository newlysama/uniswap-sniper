# Library imports
import json
import requests

# Local imports
from src.Class import Info, Pair
from src.Service.TransactionBuilder import TransactionBuilder


class PairChecker :
    def __init__(self, info : Info, pair : Pair, tx : dict):
        self.info = info
        self.pair = pair
        self.tx = tx
        self.temper_api_endpoint = "http://localhost:8080/api/v1/simulate-bundle"

    def __del__(self):
        return

    def checkLiquidity(self, initialReserves):
        if self.pair.weth_place == 0:
            return initialReserves[0] >= 5000000000000000000 # 0.5 eth in wei
        else:
            return initialReserves[1] >= 5000000000000000000
    def checkScam(self):
        try:
            checkScamBundle = TransactionBuilder.buildCheckScamBundle(self.info, self.pair, self.tx)
        except Exception as e:
            raise Exception(f"bundle building failed : {str(e)}")

        try:
            response = requests.post(self.temper_api_endpoint, json=checkScamBundle)
        except Exception as e:
            raise Exception(f"sending simulate bundle request failed : {str(e)}")

        if response.status_code == 200:
            simulation_result = response.json()
            print(json.dumps(simulation_result))
        else:
            raise Exception(f"simulate bundle request failed with status {response.status_code} : {response.text}")
