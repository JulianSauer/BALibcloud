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
        self.init_driver()

    @abc.abstractmethod
    def init_driver(self):
        """Initializes the driver."""
        return

    def get_connection(self):
        if self.connection is None | self.driver is None:
            self.init_driver()
        return self.connection

    def launch_node(self, **kwds):
        if 'image' in kwds and 'size' in kwds:
            date = str(datetime.datetime.now().strftime('%d%m%Y-%H%M%S'))
            if 'location' in kwds and 'options' in kwds:
                self.connection.create_node(name="libcloud" + date,
                                            image=kwds['image'],
                                            size=kwds['size'], location=kwds['location'],
                                            ex_create_attr=kwds['options'])
            else:
                self.connection.create_node(name="libcloud" + date, image=kwds['image'],
                                            size=kwds['size'])

    @abc.abstractmethod
    def create_node(self):
        """Creates a node."""
        return

    def print(self):
        try:
            nodes = self.driver.list_nodes(self.connection)
            print(nodes)
        except NotImplementedError:
            pass

    def destroy_nodes(self):
        try:
            nodes = self.driver.list_nodes(self.connection)
            for node in nodes:
                self.driver.destroy_node(self.connection, node)
        except NotImplementedError:
            print("Cannot delete nodes")
