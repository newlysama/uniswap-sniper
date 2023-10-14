# Library imports
from web3 import Web3
from flashbots import flashbot
from eth_account.account import Account

# Local imports
from src.Class.Contract import Contract
from src.Class.Token import Token
from src.Class.Wallet import Wallet


class Info :
    def __init__(self, w3 : Web3, router : Contract, factory : Contract, phantom : Contract, flashbot : flashbot, sniper : Wallet, signer : Account, weth : Token):
        self.w3 = w3
        self.router = router
        self.factory = factory
        self.phantom = phantom
        self.flashbot = flashbot
        self.sniper = sniper
        self.signer = signer
        self.weth = weth