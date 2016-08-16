import paramiko
from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider

from clouds.cloudprovider import CloudProvider


class AmazonWebServices(CloudProvider):
    def __init__(self):
        super().__init__('awsUser', 'awsPassword')

    def create_node(self):
        images = self.connection.list_images()
        sizes = self.connection.list_sizes()
        image = [i for i in images if 'ubuntu-trusty-14.04' in i.name][0]
        size = [s for s in sizes if s.ram == 512][0]
        node = self.connection.create_node(name=self.get_node_name(), image=image,
                                           size=size, ex_keyname='fog', ex_assign_pulic_ip=True)
        self.connection.wait_until_running([node])

        elastic_ip = self.connection.ex_allocate_address()
        self.connection.ex_associate_address_with_node(node, elastic_ip)
        host = 'ec2-' + elastic_ip.ip.replace('.', '-') + '.compute-1.amazonaws.com'
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        key = paramiko.RSAKey.from_private_key_file('/home/julian/.ssh/fog.pem')
        ssh.connect(host, username='ubuntu', pkey=key)
        sftp = ssh.open_sftp()
        sftp.put('/home/julian/Documents/BALibcloud/resources/install.sh', '/home/ubuntu/install.sh')
        sftp.close()

    def init_driver(self):
        self.driver = get_driver(Provider.EC2)
        self.connection = self.driver(self.user, self.password)
