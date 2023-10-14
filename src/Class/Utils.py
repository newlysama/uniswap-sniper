class Utils:
    def __new__(cls):
        return

    @staticmethod
    def printAmount(amountInWei : int, decimals : int) -> str :
        amount = amountInWei / (10 ** decimals)
        integer_part, decimal_part = str(amount).split('.')
        integer_part_with_commas = "{:,}".format(int(integer_part))
        return f"{integer_part_with_commas}.{decimal_part}"