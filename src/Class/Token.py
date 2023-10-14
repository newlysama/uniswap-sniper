# Library imports
from web3 import Web3
import json

class Token:
    def __init__(self, w3 : Web3, tokenAddress : str):
        try:
            self.address = w3.to_checksum_address(tokenAddress)

            if tokenAddress == "0x7b79995e5f793A07Bc00c21412e50Ecae098E7f9":
                f = open("resources/abis/weth.json", 'r')
                self.abi = json.load(f)
                f.close()

            else:
                f = open("resources/abis/erc20.json", 'r')
                self.abi = json.load(f)
                f.close()

            self.contract = w3.eth.contract(address=self.address, abi=self.abi)
            self.decimals = self.contract.functions.decimals().call()
            self.symbol = self.contract.functions.symbol().call()
        except Exception as e:
            raise Exception(f"Token.__init__() : {str(e)}")
    
    def __del__(self):
        return

    # Return self.token balance of a specific contract address
    def getBalance(self, contractAddress : str):
        return self.contract.functions.balanceOf(address=self.w3.to_checksum_address(contractAddress))

    def decodeTxInput(self, txInput):
        return self.contract.decode_function_input(txInput)