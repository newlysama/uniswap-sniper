# Library imports
from eth_account import Account
from web3 import Web3

from src.Class import Token


class Wallet:
    def __init__(self, w3 : Web3, weth : Token, address : str, privateKey : str):
        self.w3 = w3
        self.weth = weth
        self.address = address
        self.privateKey = privateKey

        try:
            self.account = Account.from_key(privateKey)
        except Exception as e:
            raise Exception(f"Wallet.__init__() : {str(e)}")

    # Return wallet's eth balance
    def getEthBalance(self) -> int:
        return self.w3.eth.get_balance(self.address)

    # Return wallet's token balance
    def getTokenBalance(self, token : Token) -> int:
        return token.contract.functions.balanceOf(self.w3.to_checksum_address(self.address)).call()

    def getWethBalance(self) -> int:
        return self.getTokenBalance(self.weth)
