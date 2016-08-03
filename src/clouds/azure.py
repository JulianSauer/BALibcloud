from libcloud.common.types import LibcloudError
from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider

from clouds.cloudprovider import CloudProvider


class MicrosoftAzure(CloudProvider):
    def __init__(self):
        super().__init__('maUser', 'maPassword')

    def init_driver(self):
        self.driver = get_driver(Provider.AZURE)
        self.connection = self.driver(self.user, self.password)

    def create_node(self):
        images = self.connection.list_images()
        sizes = self.connection.list_sizes()
        image = [i for i in images if 'Debian' in i.name][0]
        size = [s for s in sizes if 'Small' in s.name][0]
        super().launch_node(image=image, size=size, ex_cloud_service_name='libcloudservice')

    def list_nodes(self):
        try:
            nodes = self.driver.list_nodes(self.connection, ex_cloud_service_name='libcloudservice')
            print(nodes)
        except NotImplementedError:
            print('Cannot list nodes')

    def destroy_nodes(self):
        try:
            nodes = self.driver.list_nodes(self.connection, ex_cloud_service_name='libcloudservice')
            for node in nodes:
                try:
                    self.driver.destroy_node(self.connection, node)
                except LibcloudError as error:
                    print('Could not delete a node. ' + error.value)
        except NotImplementedError:
            print('Cannot delete nodes')
