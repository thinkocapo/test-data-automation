import requests
import yaml
import string
import random
import urlparse

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

with open('../endpoints.yaml', 'r') as stream:
    data_loaded = yaml.safe_load(stream)
    endpoints = data_loaded['backend_endpoints']

    for endpoint in endpoints:
        requests.get(urlparse.urljoin(endpoint, 'handled'))
        requests.get(urlparse.urljoin(endpoint, 'unhandled'))
        requests.post(urlparse.urljoin(endpoint, 'checkout'),
            json={
                "email": "%s@yahoo.com" % id_generator().lower(),
                "cart": [{
                    "id": "wrench",
                    "name": "Wrench",
                    "price": 500
                }, {
                    "id": "wrench",
                    "name": "Wrench",
                    "price": 500
                }]
            }
        )


