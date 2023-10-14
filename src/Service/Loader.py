# Library imports
import logging

from web3 import Web3
from flashbots import flashbot
from eth_account.account import Account
import json

# Local imports
from src.Class.Contract import Contract
from src.Class.Token import Token
from src.Class.Info import Info
from src.Class.Wallet import Wallet
from src.GlobalLogger import logger

class Loader :
    def __init__(self):
        self.nodePath = "resources/api.json"
        self.contractsPath = "resources/contract_addresses.json"
        self.abisPath = "resources/abis/"
        self.accountsPath = "resources/accounts.json"
        self.flashbotsRelayURL = "https://boost-relay.flashbots.net"
        self.w3 = None
    
    def __del__(self):
        return
    
    def __loadWeb3Connection(self):
        try :
            nodeFile = open(self.nodePath, 'r')
            node = json.load(nodeFile)
            w3 = Web3(Web3.HTTPProvider(node["infura"]["mainnet"]))
            
            nodeFile.close()

            if not w3.is_connected():
                raise Exception("Loader.__loadWeb3Connection() : w3 nod is not connected.")
            
            self.w3 = w3
        except Exception as e:
            raise Exception(f"Loader.__loadWeb3Connection() : {str(e)}")
     
    def __loadUniswapRouter(self):
        try :
            contractsFile = open(self.contractsPath, 'r')
            contracts = json.load(contractsFile)
            routerAddress = contracts["eth"]["uniswapv2_router"]
            
            routerAbiFile = open(self.abisPath + "uniswapv2_router.json", 'r')
            routerAbi = json.load(routerAbiFile)
            
            contractsFile.close()
            routerAbiFile.close()
            
            return Contract(self.w3, routerAddress, routerAbi)
            
        except Exception as e:
            raise Exception(f"Loader.__loadUniswapRouter() : {str(e)}")
        
    def __loadUniswapFactory(self):
        try :
            contractsFile = open(self.contractsPath, 'r')
            contracts = json.load(contractsFile)
            factoryAddress = contracts["eth"]["uniswapv2_factory"]
            
            factoryAbiFile = open(self.abisPath + "uniswapv2_factory.json", 'r')
            factoryAbi = json.load(factoryAbiFile)
            
            contractsFile.close()
            factoryAbiFile.close()
            
            return Contract(self.w3, factoryAddress, factoryAbi)
            
        except Exception as e:
            raise Exception(f"Loader.__loadUniswapFactory() : {str(e)}")
        
    def __loadPhantom(self):
        try :
            contractsFile = open(self.contractsPath, 'r')
            contracts = json.load(contractsFile)
            phantomAddress = contracts["eth"]["phantom"]
            
            phantomAbiFile = open(self.abisPath + "phantom.json", 'r')
            phantomAbi = json.load(phantomAbiFile)
            
            contractsFile.close()
            phantomAbiFile.close()
            
            return Contract(self.w3, phantomAddress, phantomAbi)
            
        except Exception as e:
            raise Exception(f"Loader.__loadPhantom() : {str(e)}")

    def __loadWeth(self):
        try:
            contractsFile = open(self.contractsPath, 'r')
            contracts = json.load(contractsFile)
            wethAddress = contracts["eth"]["weth"]

            return Token(self.w3, wethAddress, True)
        except Exception as e:
            raise Exception(f"Loader.__loadWeth() : {str(e)}")
        
    def __loadSniperAccount(self, weth : Token):
        try :
            accountsFile = open(self.accountsPath, 'r')
            accountsJson = json.load(accountsFile)
            address = accountsJson["sniper"]["address"]
            privateKey = accountsJson["sniper"]["private_key"]

            accountsFile.close()

            return Wallet(self.w3, weth, address, privateKey)
        except Exception as e:
            raise Exception(f"Loader.__loadSniperAccount() : {str(e)}")
    
    def __loadSignerAccount(self):
        try :
            accountsFile = open(self.accountsPath, 'r')
            privateKey = json.load(accountsFile)["signer"]["private_key"]

            accountsFile.close()

            return Account.from_key(privateKey)
        except Exception as e:
            raise Exception(f"Loader.__loadSignerAccount() : {str(e)}")

    def __loadFlashbotsConnection(self, signer : Account):
        try :
            return flashbot(self.w3, signer, self.flashbotsRelayURL)
        except Exception as e:
            raise Exception(f"Loader.__loadFlashbotsConnection() : {str(e)}")
    
    def loadInfo(self):
        try :
            logger.info('Establishing web3 connection...')
            self.__loadWeb3Connection()
            logger.success("Web3 connection established.")

            logger.info('Loading Uniswap router...')
            router = self.__loadUniswapRouter()
            logger.success("Router loaded.")

            logger.info('Loading Uniswap factory...')
            factory = self.__loadUniswapFactory()
            logger.success("Factory loaded.")

            logger.info('Loading Phantom contract...')
            phantom = self.__loadPhantom()
            logger.success("Phantom loaded.")

            logger.info('Loading Weth contract...')
            weth = self.__loadWeth()
            logger.success("WETH loaded.")

            logger.info('Loading Sniper account...')
            sniper = self.__loadSniperAccount(weth)
            logger.success("Sniper account loaded.")

            logger.info('Loading Signer account...')
            signer = self.__loadSignerAccount()
            logger.success("Signer account loaded.")

            logger.info('Loading Flashbots connection...')
            flashbots = self.__loadFlashbotsConnection(signer)
            logger.success("Flashbots loaded.")

            return Info(self.w3, router, factory, phantom, flashbots, sniper, signer, weth)

        except Exception as e:
            raise e