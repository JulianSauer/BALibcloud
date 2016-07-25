from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider
import libcloud.security

from accounts import Accounts
from clouds.azure import MicrosoftAzure
from clouds.profitbricks import ProfitBricks
from clouds.digitalocean import DigitalOcean
from clouds.aws import AmazonWebServices
from clouds.gce import GoogleComputeEngine


def do_test_operations(cloud):
    cloud.print()
    print("Adding a node...")
    cloud.create_node()
    print("done.\n")
    cloud.print()
    print("Removing all nodes...")
    cloud.destroy_nodes()
    print("done.\n")
    cloud.print()


accounts = Accounts()
do_test_operations(AmazonWebServices(accounts))
do_test_operations(DigitalOcean(accounts))
do_test_operations(GoogleComputeEngine(accounts))
do_test_operations(ProfitBricks(accounts))
do_test_operations(MicrosoftAzure(accounts))
