import urllib.request


def get_my_external_ip():
    external_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
    result = 'Server IP: {0}'.format(external_ip)

    return result
