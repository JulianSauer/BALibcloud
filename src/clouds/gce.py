from libcloud.compute.types import Provider

from clouds.cloudprovider import CloudProvider


class GoogleComputeEngine(CloudProvider):
    def __init__(self):
        super().__init__('gceUser', 'gcePassword', Provider.GCE)
        self._connection = self._driver(self._user, self._password, datacenter='europe-west1-d', project='jclouds-1376')

    def _create_node(self):
        images = self._connection.list_images()
        sizes = self._connection.list_sizes()
        image = [i for i in images if 'ubuntu-1404' in i.name][0]
        for size in sizes:
            print(size.name)
        size = [s for s in sizes if 'micro' in s.name][0]
        self._connection.deploy_node(name=self._get_node_name(), image=image, size=size,
                                     script='/home/julian/Documents/BALibcloud/resources/install.sh')
