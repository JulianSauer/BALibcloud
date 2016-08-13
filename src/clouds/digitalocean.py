from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider

from clouds.cloudprovider import CloudProvider


class DigitalOcean(CloudProvider):
    def __init__(self):
        super().__init__('doUser', 'doPassword')

    def create_node(self):
        images = self.connection.list_images()
        sizes = self.connection.list_sizes()
        image = [i for i in images if i.name == '14.04.5 x64'][0]
        size = [s for s in sizes if s.ram == 512][0]
        location = self.connection.list_locations()[0]
        self.connection.create_node(name=self.get_node_name(), image=image, size=size, location=location)

    def init_driver(self):
        self.driver = get_driver(Provider.DIGITAL_OCEAN)
        self.connection = self.driver(self.password, api_version='v2')
