# Local imports

from src.Class import Pair
from src.Class import Token
from src.Class import Info
from src.GlobalLogger import logger
from src.Service.PairProcessor import PairProcessor


class MempoolListener:
    def __init__(self, info: Info):
        self.info = info
        self.processedTx = set()

    # Check if addLiquidityETH is called on an already existent pair
    def checkAddLiquidityETH(self, decodedTxInput: dict):
        # Extract needed infos
        w3 = self.info.w3
        factory = self.info.factory
        weth = self.info.weth

        zeroAddress = w3.to_checksum_address("0x0000000000000000000000000000000000000000")
        tokenAddress = w3.to_checksum_address(decodedTxInput[1]['token'])
        logger.debug(f"Token address : {str(tokenAddress)}")

        try:
            pairAddress = factory.contract.functions.getPair(tokenAddress, weth.address).call()
        except Exception as e:
            raise Exception(f"Could not call getPair : {str(e)}")

        if pairAddress == zeroAddress:  # If the pair does not already exist
            return True
        else:  # If the pair already exists, check that has no liquidity
            try:
                token = Token(w3, tokenAddress)
            except Exception as e:
                raise Exception(f"Could not create Token : {str(e)}")
            try:
                pair = Pair(weth, token, 0)
                pair.setContract(w3, pairAddress)
                b = pair.get_reserves()[0] == 0 and pair.get_reserves()[1] == 0

                if b:
                    logger.debug(f"Pair already exists. Reserves : {pair.get_reserves()} || Address : {pairAddress}")

                del pair
                return b
            except Exception as e:
                raise Exception(f"Could no create pair : {str(e)}")

    # Same as checkAddLiquidityETH but here wa also have to check if one of the tokens is WETH
    def checkAddLiquidity(self, decodedTxInput: dict):
        # Extract needed infos
        w3 = self.info.w3
        factory = self.info.factory
        weth = self.info.weth

        if w3.to_checksum_address(decodedTxInput[1]['tokenA']) == weth.address:
            weth_place = 0
            token_place = "tokenB"
        elif  w3.to_checksum_address(decodedTxInput[1]['tokenA']) == weth.address:
            weth_place = 1
            token_place = "tokenA"
        else:
            logger.debug(f"No WETH is this pair")
            return False

        zeroAddress = w3.to_checksum_address("0x0000000000000000000000000000000000000000")
        tokenAddress = w3.to_checksum_address(decodedTxInput[1][token_place])
        logger.debug(f"Token address : {str(tokenAddress)}")

        try :
            pairAddress = factory.contract.functions.getPair(tokenAddress, weth.address).call()
        except Exception as e:
            raise Exception(f"Could not call getPair : {str(e)}")

        if pairAddress == zeroAddress:
            return True

        else:
            try:
                token = Token(w3, tokenAddress)
            except Exception as e:
                raise Exception(f"Could not create Token : {str(e)}")
            try:
                pair = Pair(weth, token, weth_place)
                pair.setContract(w3, pairAddress)
                b = pair.get_reserves()[0] == 0 and pair.get_reserves()[1] == 0

                logger.debug(f"Pair already exists. Reserves : {pair.get_reserves()} || Address : {pairAddress}")

                del pair
                return b
            except Exception as e:
                raise Exception(f"Could no create pair : {str(e)}")




    # When addLiquidityETH is detected, check if it's valid, and build a new Pair object
    def processAddLiquidityETH(self, txInput: str):
        # Extract needed infos
        w3 = self.info.w3
        weth = self.info.weth
        router = self.info.router

        try:
            decodedTxInput = router.decodeTxInput(txInput)
        except Exception as e:
            raise Exception(f"could not decode tx input : [{str(e)}]")

        try:
            b = self.checkAddLiquidityETH(decodedTxInput)
        except Exception as e:
            raise Exception(f"exception raised in checkAddLiquidityETH : [{str(e)}]")
        if b:
            try:
                token = Token(w3, decodedTxInput[1]['token'])
                logger.debug(f"Pair created with addLiquidityETH: {token.symbol}/WETH")
            except Exception as e:
                raise Exception(f"exception raised during pair creation : [{str(e)}]")

            try:
                # Check the WETH place in the pair
                if token.address > weth.address:
                    return Pair(weth, token, 0)
                else:
                    return Pair(weth, token, 1)

            except Exception as e:
                raise Exception(f"exception raised during token creation : [{str(e)}]")

    def processTokenLiquidityAdding(self, tx: dict):
        # Extract needed infos
        w3 = self.info.w3
        weth = self.info.weth

        logger.debug("Processing Token liquidity adding...")

        try:
            token = Token(w3, tx['to'])
        except Exception as e:
            raise Exception(f"exception raised during token creation : [{str(e)}]")

        logger.debug(f"Token address : {str(tx['to'])}")
        logger.debug(f"Pair created with OpenTrading/EnableTrading: {token.symbol}/WETH")

        try:
            # Check the WETH place in the pair
            if token.address > weth.address:
                return Pair(weth, token, 0)
            else:
                return Pair(weth, token, 1)

        except Exception as e:
            raise Exception(f"exception raised during pair creation : [{str(e)}]")

    def listen(self):
        # Extract needed infos
        w3 = self.info.w3
        router = self.info.router

        numberTx = 0

        logger.info(f"Listening to the mempool...")

        while True:
            if numberTx == 10000:
                self.processedTx.clear()
                numberTx = 0

            try:
                # Get pending block
                pendingBlock = w3.eth.get_block('pending', full_transactions=True)
            except Exception as e:
                logger.error(f"ERROR :could not get latest block : [{str(e)}]")
                logger.info(f"Listening to the mempool...")
                continue

                # Get pending transactions
            pendingTx = pendingBlock['transactions']

            for tx in pendingTx:
                # Check if the tx has already been processed
                if tx['hash'] in self.processedTx:
                    continue  # Skip it

                txInput = tx['input'].hex()

                if tx.get('to'):
                    # Check if the tx is passed to Uniswap router
                    if w3.to_checksum_address(tx['to']) == router.address:
                        # Check if the tx is addLiquidityETH
                        if txInput.startswith('0xf305d719'):
                            logger.debug(f"addLiquidityETH detected : {tx['hash'].hex()}")
                            try:
                                pair = self.processAddLiquidityETH(txInput)
                            except Exception as e:
                                logger.error(f"ERROR in processAddLiquidityETH : {str(e)}")
                                numberTx += 1
                                self.processedTx.add(tx['hash'])
                                logger.info("Listening to the mempool...")
                                continue

                            # If pair == None, means tx failed, so skip this pair
                            if not pair:
                                logger.debug("Pair not valid, skipping.")
                                numberTx += 1
                                self.processedTx.add(tx['hash'])

                                logger.info("Listening to the mempool...")
                                continue

                                # Processing pair
                            logger.status("STARTING PAIR PROCESSING")
                            pairProcessor = PairProcessor(self.info, pair, tx)
                            pairProcessor.processPair()

                            # Continue listening the mempool
                            numberTx += 1
                            self.processedTx.add(tx['hash'])
                            logger.info("Listening to the mempool...")
                            continue

                        # Check if the tx is addLiquidity
                        elif txInput.startswith('0xf305d719'):
                            continue

                        else:
                            numberTx += 1
                            self.processedTx.add(tx['hash'])
                            continue

                    # If the tx is not sent to the router, check token liquidity adding functions
                    elif txInput.startswith('0xc9567bf9') or txInput.startswith('0x8a8c523c'):  # openTrading or enableTrading function signatures
                        logger.debug(f"OpenTrading/EnableTrading detected : {tx['hash'].hex()}")
                        try:
                            pair = self.processTokenLiquidityAdding(tx)
                        except Exception as e:
                            logger.error(f"ERROR during processTokenLiquidityAdding : {str(e)}")
                            numberTx += 1
                            self.processedTx.add(tx['hash'])
                            logger.info("Listening to the mempool...")
                            continue

                            # If pair == None, means tx failed, so skip this pair
                        if not pair:
                            logger.debug("Pair not valid, skipping.")
                            numberTx += 1
                            self.processedTx.add(tx['hash'])
                            logger.info("Listening to the mempool...")
                            continue

                        # Processing pair
                        logger.status("STARTING PAIR PROCESSING")
                        pairProcessor = PairProcessor(self.info, pair, tx)
                        pairProcessor.processPair()

                        # Continue listening the mempool
                        numberTx += 1
                        self.processedTx.add(tx['hash'])
                        logger.info("Listening to the mempool...")
                        continue

                    # If the transaction is not adding liquidity, continue listening to the mempool
                    else:
                        numberTx += 1
                        self.processedTx.add(tx['hash'])
                        continue
                else:
                    self.processedTx.add(tx['hash'])
                    numberTx += 1
                    continue