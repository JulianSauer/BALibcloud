import abc
import datetime

import libcloud.security
from libcloud.compute.providers import get_driver

from accounts import Accounts


class CloudProvider(object):
    __metaclass__ = abc.ABCMeta

    user = None
    password = None

    driver = None
    connection = None

    def __init__(self, userKey, passwordKey, provider):
        accounts = Accounts()
        self.user = accounts.get_value_for(userKey)
        self.password = accounts.get_value_for(passwordKey)

        # libcloud.security.CA_CERTS_PATH = ['C:/Users/jsauer/AppData/Roaming/ca-bundle.crt']  # Windows requires certificates explicitly
        self.driver = get_driver(provider)

    @abc.abstractmethod
    def create_node(self):
        """Creates a node."""
        return

    def destroy_nodes(self):
        try:
            nodes = self.driver.list_nodes(self.connection)
            for node in nodes:
                self.driver.destroy_node(self.connection, node)
        except NotImplementedError:
            print('Cannot delete nodes')

    def do_test_operations(self):
        self.list_nodes()
        print('Removing all nodes...')
        self.destroy_nodes()
        print('done.\n')
        self.list_nodes()
        print('Adding a node...')
        self.create_node()
        print('done.\n')
        self.list_nodes()

    def get_node_name(self):
        date = str(datetime.datetime.now().strftime('%d%m%Y-%H%M%S'))
        return 'libcloud' + date

    def list_nodes(self):
        try:
            nodes = self.driver.list_nodes(self.connection)
            print(nodes)
        except NotImplementedError:
            print('Cannot list nodes')
