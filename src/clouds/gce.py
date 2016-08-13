from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider

from clouds.cloudprovider import CloudProvider


class GoogleComputeEngine(CloudProvider):
    def __init__(self):
        super().__init__('gceUser', 'gcePassword')

    def create_node(self):
        images = self.connection.list_images()
        sizes = self.connection.list_sizes()
        image = [i for i in images if 'ubuntu-1404' in i.name][0]
        size = [s for s in sizes if 'micro' in s.name][0]
        self.connection.deploy_node(name=self.get_node_name(), image=image, size=size,
                                    script='/home/julian/Documents/BALibcloud/resources/install.sh')

    def init_driver(self):
        self.driver = get_driver(Provider.GCE)
        self.connection = self.driver(self.user, self.password, datacenter='europe-west1-d', project='jclouds-1376')
