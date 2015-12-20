import pyeapi
import replicants

import os

os.environ['REPLICANTS_FOLDER'] = os.path.abspath('./command_error')


def main():
    connection = pyeapi.client.connect(
        transport='https',
        host='localhost',
        username='vagrant',
        password='vagrant',
        port=12443
    )
    connection = replicants.patch_node(connection, 'eos', 'record')
    node = pyeapi.client.Node(connection)

    try:
        print node.run_commands(['show ip route', 'show ip bgp neighbors', 'show lldp neighbors'], encoding='json')
    except pyeapi.eapilib.CommandError as e:
        print e.get_trace()


if __name__ == "__main__":
    main()
