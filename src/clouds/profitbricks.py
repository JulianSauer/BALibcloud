from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider

from clouds.cloudprovider import CloudProvider


class ProfitBricks(CloudProvider):
    def __init__(self):
        super().__init__('pbUser', 'pbPassword')

    def create_node(self):
        images = self.connection.list_images()
        sizes = self.connection.list_sizes()
        image = [i for i in images if 'Ubuntu-14.04' in i.name][0]
        size = [s for s in sizes if s.ram == 1024][0]
        self.connection.create_node(name=self.get_node_name(), image=image, size=size)

    def init_driver(self):
        self.driver = get_driver(Provider.PROFIT_BRICKS)
        self.connection = self.driver(self.user, self.password)
