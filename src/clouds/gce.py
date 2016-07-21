from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider

from clouds.cloudprovider import CloudProvider


class GoogleComputeEngine(CloudProvider):
    def __init__(self, accounts):
        user = accounts.get_value_for('gceUser')
        password = accounts.get_value_for('gcePassword')
        super().__init__(user, password)

    def init_driver(self):
        self.driver = get_driver(Provider.GCE)
        self.connection = self.driver(self.user, self.password, project='jclouds')

    def create_node(self):
        images = self.connection.list_images()
        sizes = self.connection.list_sizes()
        image = [i for i in images if i.name == "Ubuntu"][0]
        size = [s for s in sizes if s.ram == 512][0]
        super().launch_node(image=image, size=size)
