from web3 import Web3
import json

class Contract :
    def __init__(self, w3 : Web3, address : str, abi : json.loads) :
        self.address = w3.to_checksum_address(address)
        self.abi = abi
        self.contract = w3.eth.contract(address=self.address, abi=self.abi)

    def decodeTxInput(self, txInput):
        return self.contract.decode_function_input(txInput)
