from libcloud.compute.types import Provider

from clouds.cloudprovider import CloudProvider


class DigitalOcean(CloudProvider):
    def __init__(self):
        super().__init__('doUser', 'doPassword', Provider.DIGITAL_OCEAN)
        self._connection = self._driver(self._password, api_version='v2')

    def _create_node(self):
        images = self._connection.list_images()
        sizes = self._connection.list_sizes()
        image = [i for i in images if '14.04' in i.name][0]
        size = [s for s in sizes if '512mb' in s.name][0]
        location = self._connection.list_locations()[0]
        self._connection.create_node(name=self._get_node_name(), image=image, size=size, location=location)
