# Local imports
from eth_abi import abi

from src.Service import Loader
from src.GlobalLogger import logger
from src.Service.MempoolListener import MempoolListener

from src.Class import Token, Utils, Pair
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

"""
# Load infos
loader = Loader()
info = loader.loadInfo()

# Extract needed infos
w3 = info.w3
router = info.router
factory = info.factory
weth = info.weth
phantom = info.phantom
sniper = info.sniper

# Api
endpoint = "http://localhost:8080/api/v1/simulate"

# Token to snipe
#token = Token(w3, "")

# Pair
pairAddress = factory.functions.getPair(token.address, weth.address)
pair = Pair(weth, token, 0)
pair.setContract(w3, pairAddress)
reserves = pair.get_reserves()
print(f"Reserve 0 : {reserves[0]} || Reserve 1 : {reserves[1]} || Reserve 2 : {reserves[2]}")



# The tx we want to simulate
tx = phantom.contract.functions.checkScam("0x7334f2D4d7A014e4d74C6F9D2BC5C21adc744783").build_transaction({
    "from": sniper.address,
    "nonce": w3.eth.get_transaction_count(sniper.address),
    "gas": 300000,
    "gasPrice": w3.eth.gas_price
})

signed_tx = w3.eth.account.sign_transaction(tx, sniper.privateKey)
print(f"Tx : {tx}")
decodedInput = phantom.decodeTxInput(signed_tx[0])

# The request body

body = {
    "chainId": 1,
    "from": str(sniper.address), # My wallet address
    "to": str(phantom.address),
    "value" : "0x0",
    "data": tx['data'],
    "gasLimit": 500000,
    "stateOverrides": {
        str(phantom.address): {
            "balance": "100000000000000000000" # 10 ETH
            }
        }
    }

response = requests.post(endpoint, json=body)

if response.status_code == 200:
    simulation_result = response.json()
    returnData = simulation_result["returnData"]
    res = bytes.fromhex(returnData[2:])
    print("Simulation result : ", abi.decode(['uint256', 'uint256', 'uint256', 'uint256'], res))
else:
    raise Exception(f"simulate bundle request failed with status {response.status_code} : {response.text}")
"""
