import pyeapi
import replicants

import os
os.environ['REPLICANTS_FOLDER'] = os.path.abspath('./api_get_vlans')


def main():
    connection = pyeapi.client.connect(
        transport='https',
        host='localhost',
        username='vagrant',
        password='vagrant',
        port=12443
    )
    connection = replicants.patch_node(connection, 'eos', 'play')

    node = pyeapi.client.Node(connection)
    vlans = node.api('vlans')

    print vlans.getall()
    print node.run_commands(['show vlan'])

if __name__ == "__main__":
    main()
