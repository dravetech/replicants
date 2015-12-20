import eapimocker


def patch_node(node, os, action):
    if action not in ['record', 'play']:
        raise Exception('Unknown action: {action}'.format(action))
    if os == 'eos':
        return patch_eos(node, action)
    else:
        raise Exception('Unknown os: {os}'.format(os))


def patch_eos(node, action):
    if action == 'record':
        return eapimocker.EapiRecorder(node)
    else:
        return eapimocker.EapiPlayer(node)