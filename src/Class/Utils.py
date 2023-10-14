class Utils:
    def __new__(cls):
        return

    @staticmethod
    def printAmount(amountInWei : int, decimals : int) -> None :
        amount = amountInWei / (10 ** decimals)
        integer_part, decimal_part = str(amount).split('.')
        integer_part_with_commas = "{:,}".format(int(integer_part))
        print(f"{integer_part_with_commas}.{decimal_part}")