class Accounts:
    def __init__(self):
        global accounts
        accounts = {}
        with open("../resources/accounts.txt") as accounts_file:
            for line in accounts_file:
                key, value = line.partition("=")[::2]
                value = value[:len(value)-1]
                accounts[key.strip()] = value

    def get_value_for(self, key):
        return accounts[key]
