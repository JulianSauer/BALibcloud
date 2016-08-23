from libcloud.common.types import LibcloudError
from libcloud.compute.types import Provider

from clouds.cloudprovider import CloudProvider


class MicrosoftAzure(CloudProvider):
    service_name = 'libcloudservice'

    def __init__(self):
        super().__init__('maUser', 'maPassword', Provider.AZURE)
        self._connection = self._driver(self._user, self._password)

    def _create_node(self):
        images = self._connection.list_images()
        sizes = self._connection.list_sizes()
        image = [i for i in images if 'Ubuntu-14.04' in i.name][0]
        size = [s for s in sizes if 'Small' in s.name][0]
        self._connection.create_node(name=self._get_node_name(), image=image, size=size,
                                     ex_cloud_service_name=self.service_name)

    def _destroy_nodes(self):
        nodes = self._driver.list_nodes(self._connection, ex_cloud_service_name=self.service_name)
        for node in nodes:
            try:
                self._driver.destroy_node(self._connection, node)
            except LibcloudError as error:
                print('Could not delete a node. ' + error.value)
        print('Cannot delete nodes')

    def _list_nodes(self):
        nodes = self._driver.list_nodes(self._connection, ex_cloud_service_name=self.service_name)
        print(nodes)
