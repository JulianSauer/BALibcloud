import abc
import datetime

import libcloud.security
from libcloud.compute.providers import get_driver


class CloudProvider(object):
    __metaclass__ = abc.ABCMeta

    user = None
    password = None

    driver = None  # jclouds equivalent: ComputeServiceContext
    connection = None  # jclouds equivalent: ComputeService

    def __init__(self, user, password):
        libcloud.security.CA_CERTS_PATH = ['C:/Users/jsauer/AppData/Roaming/ca-bundle.crt']
        self.user = user
        self.password = password
        self.get_initialized_driver()

    def init_driver(self, provider):
        self.driver = get_driver(provider)
        self.connection = self.driver(self.user, self.password)

        return self.driver

    @abc.abstractmethod
    def get_initialized_driver(self):
        """Initializes a driver."""
        return

    def get_connection(self):
        if self.connection is None | self.driver is None:
            self.get_initialized_driver()
        return self.connection

    def launch_node(self, image, size):
        self.connection.create_node(name="node" + str(datetime.datetime.now()), image=image, size=size)

    @abc.abstractmethod
    def create_node(self):
        """Creates a node."""
        return

    def print(self):
        nodes = self.driver.list_nodes(self.connection)
        print(nodes)

    def destroy_nodes(self):
        nodes = self.driver.list_nodes(self.connection)
        for node in nodes:
            self.driver.destroy_node(self.connection, node)
