import abc
import datetime
import inspect
import sys

import libcloud.security
from libcloud.compute.providers import get_driver

from accounts import Accounts


class CloudProvider(object):
    __metaclass__ = abc.ABCMeta

    user = None
    password = None

    driver = None  # jclouds equivalent: ComputeServiceContext
    connection = None  # jclouds equivalent: ComputeService

    def __init__(self, userKey, passwordKey):
        accounts = Accounts()
        self.user = accounts.get_value_for(userKey)
        self.password = accounts.get_value_for(passwordKey)

        # libcloud.security.CA_CERTS_PATH = ['C:/Users/jsauer/AppData/Roaming/ca-bundle.crt'] # Uncomment if running on Linux
        try:
            self.init_driver()
        except RuntimeError:
            print('Change/remove CA_CERTS_PATH in cloudprovider.py if running into issues.')
            sys.exit()

    @abc.abstractmethod
    def init_driver(self):
        """Initializes the driver."""
        return

    def get_connection(self):
        if self.connection is None | self.driver is None:
            self.init_driver()
        return self.connection

    def launch_node(self, **kwds):
        if 'image' not in kwds or 'size' not in kwds:
            return

        if 'location' in kwds and 'options' in kwds:
            self.connection.create_node(name=self.get_node_name(),
                                        image=kwds['image'],
                                        size=kwds['size'], location=kwds['location'],
                                        ex_create_attr=kwds['options'])
        elif 'ex_cloud_service_name' in kwds:
            self.connection.create_node(name=self.get_node_name(), image=kwds['image'],
                                        size=kwds['size'], ex_cloud_service_name=kwds['ex_cloud_service_name'])
        else:
            self.connection.create_node(name=self.get_node_name(), image=kwds['image'],
                                        size=kwds['size'])

    @abc.abstractmethod
    def create_node(self):
        """Creates a node."""
        return

    def list_nodes(self):
        try:
            nodes = self.driver.list_nodes(self.connection)
            print(nodes)
        except NotImplementedError:
            print('Cannot list nodes')

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
