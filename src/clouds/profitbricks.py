from libcloud.compute.types import Provider

from clouds.cloudprovider import CloudProvider


class ProfitBricks(CloudProvider):
    def __init__(self):
        super().__init__('pbUser', 'pbPassword', Provider.PROFIT_BRICKS)
        self._connection = self._driver(self._user, self._password)

    def _create_node(self):
        images = self._connection.list_images()
        sizes = self._connection.list_sizes()
        image = [i for i in images if 'Ubuntu-14.04' in i.name][0]
        size = [s for s in sizes if 'Small' in s.name][0]
        self._connection.create_node(name=self._get_node_name(), image=image, size=size)
