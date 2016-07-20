from aws import AmazonWebServices


class Main:
    def main(self):
        aws = AmazonWebServices()
        aws.print()
        aws.create_node()
        aws.print()
        aws.destroy_nodes()
        aws.print()


Main().main()
