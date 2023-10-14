# Library imports
from web3 import Web3
import json

#Local imports
from src.Class.Token import Token

class Pair:
    def __init__(self, weth : Token, token : Token, weth_place : int):
        try:
            # Load the pair ABI
            file = open("resources/abis/pair.json", 'r')
            pair_abi = json.load(file)
            file.close()

            self.address = None
            self.abi = pair_abi
            self.contract = None
            self.token = token
            self.weth = weth
            self.weth_place = weth_place # When a pair is created, we don't know if the token is the first or second one, so we need to know it
        except Exception as e:
            raise Exception(f"Pair.__init__() : {str(e)}")

    def __del__(self):
        return
    
    def get_reserves(self):
        try:
            return self.contract.functions.getReserves().call()
        except Exception as e:
            raise Exception(f"Pair.getReserves() : {str(e)}")

    def decodeTxInput(self, txInput):
        return self.contract.decode_function_input(txInput)

    def setContract(self, w3 : Web3, address : str):
        self.address = w3.to_checksum_address(address)
        self.contract = w3.eth.contract(address=self.address, abi=self.abi)