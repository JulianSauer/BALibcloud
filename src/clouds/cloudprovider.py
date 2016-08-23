import abc
import datetime

import libcloud.security
from libcloud.compute.providers import get_driver

from accounts import Accounts


class CloudProvider(object):
    __metaclass__ = abc.ABCMeta

    _user = None
    _password = None

    _driver = None
    _connection = None

    def __init__(self, user_key, password_key, provider):
        accounts = Accounts()
        self._user = accounts.get_value_for(user_key)
        self._password = accounts.get_value_for(password_key)

        # libcloud.security.CA_CERTS_PATH = ['C:/Users/jsauer/AppData/Roaming/ca-bundle.crt']  # Windows requires certificates explicitly
        self._driver = get_driver(provider)

    @abc.abstractmethod
    def _create_node(self):
        """Creates a node."""
        return

    def _destroy_nodes(self):
        try:
            nodes = self._driver.list_nodes(self._connection)
            for node in nodes:
                self._driver.destroy_node(self._connection, node)
        except NotImplementedError:
            print('Cannot delete nodes')

    def _get_node_name(self):
        date = str(datetime.datetime.now().strftime('%d%m%Y-%H%M%S'))
        return 'libcloud' + date

    def _list_nodes(self):
        try:
            nodes = self._driver.list_nodes(self._connection)
            print(nodes)
        except NotImplementedError:
            print('Cannot list nodes')

    def do_test_operations(self):
        self._list_nodes()
        print('Removing all nodes...')
        self._destroy_nodes()
        print('done.\n')
        self._list_nodes()
        print('Adding a node...')
        self._create_node()
        print('done.\n')
        self._list_nodes()
