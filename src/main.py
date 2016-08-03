from clouds.aws import AmazonWebServices
from clouds.azure import MicrosoftAzure
from clouds.digitalocean import DigitalOcean
from clouds.gce import GoogleComputeEngine
from clouds.profitbricks import ProfitBricks

AmazonWebServices().do_test_operations()
DigitalOcean().do_test_operations()
GoogleComputeEngine().do_test_operations()
ProfitBricks().do_test_operations()  # TODO: Node creation currently fails
MicrosoftAzure().do_test_operations()
