from fabric import api

def local(command, capture=False):
    return api.local(command, shell="/bin/bash", capture=capture)

