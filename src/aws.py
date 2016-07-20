import libcloud.security
from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider
from accounts import Accounts
from cloudprovider import CloudProvider


class AmazonWebServices(CloudProvider):
    def __init__(self):
        accounts = Accounts()
        user = accounts.get_value_for("awsUser")
        password = accounts.get_value_for("awsPassword")
        super().__init__(user, password)

    def get_initialized_driver(self):
        return self.init_driver(Provider.EC2)

    def create_node(self):
        images = self.connection.list_images()
        sizes = self.connection.list_sizes()
        image = [i for i in images if i.name == "AmazonLinux"][0]
        size = [s for s in sizes if s.ram == 512][0]
        super().launch_node(image, size)
