import paramiko
from libcloud.compute.types import Provider

from clouds.cloudprovider import CloudProvider


class AmazonWebServices(CloudProvider):
    def __init__(self):
        super().__init__('awsUser', 'awsPassword', Provider.EC2)
        self._connection = self._driver(self._user, self._password)

    def _create_node(self):
        images = self._connection.list_images()
        sizes = self._connection.list_sizes()
        image = [i for i in images if i.id == 'ami-2d39803a'][0]
        size = [s for s in sizes if 'Nano Instance' in s.name][0]
        node = self._connection.create_node(name=self._get_node_name(), image=image,
                                            size=size, ex_keyname='fog', ex_assign_pulic_ip=True)
        self._connection.wait_until_running([node])

        elastic_ip = self._connection.ex_allocate_address()
        self._connection.ex_associate_address_with_node(node, elastic_ip)
        host = 'ec2-' + elastic_ip.ip.replace('.', '-') + '.compute-1.amazonaws.com'
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        key = paramiko.RSAKey.from_private_key_file('/home/julian/.ssh/fog.pem')
        ssh.connect(host, username='ubuntu', pkey=key)
        sftp = ssh.open_sftp()
        sftp.put('/home/julian/Documents/BALibcloud/resources/install.sh', '/home/ubuntu/install.sh')
        sftp.close()
        ssh.exec_command('bash /home/ubuntu/install.sh')
