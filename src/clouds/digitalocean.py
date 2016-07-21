from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider

from clouds.cloudprovider import CloudProvider


class DigitalOcean(CloudProvider):
    def __init__(self, accounts):
        user = accounts.get_value_for("doUser")
        password = accounts.get_value_for("doPassword")
        super().__init__(user, password)

    def init_driver(self):
        self.driver = get_driver(Provider.DIGITAL_OCEAN)
        self.connection = self.driver(self.password, api_version='v2')

    def create_node(self):
        images = self.connection.list_images()
        sizes = self.connection.list_sizes()
        image = images[1]  # DigitalOcean images have useless names
        size = [s for s in sizes if s.ram == 512][0]
        location = self.connection.list_locations()[0]
        options = {'ssh_keys': []}
        super().launch_node(image=image, size=size, location=location, options=options)
