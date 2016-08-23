# Helper class for reading account data from files.
#
# Requires the file BALibcloud/resources/accounts.txt
# with key value pairs in the format:
# key=value


class Accounts:
    accounts = {}

    def __init__(self):
        with open('../resources/accounts.txt') as accounts_file:
            for line in accounts_file:
                key, value = line.partition('=')[::2]
                value = value[:len(value) - 1]
                self.accounts[key.strip()] = value

    def get_value_for(self, key):
        return self.accounts[key]
