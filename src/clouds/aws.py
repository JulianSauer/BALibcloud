from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider

from clouds.cloudprovider import CloudProvider


class AmazonWebServices(CloudProvider):
    def __init__(self, accounts):
        user = accounts.get_value_for("awsUser")
        password = accounts.get_value_for("awsPassword")
        super().__init__(user, password)

    def init_driver(self):
        self.driver = get_driver(Provider.EC2)
        self.connection = self.driver(self.user, self.password)

    def create_node(self):
        images = self.connection.list_images()
        sizes = self.connection.list_sizes()
        image = [i for i in images if i.name == "AmazonLinux"][0]
        size = [s for s in sizes if s.ram == 512][0]
        super().launch_node(image=image, size=size)
