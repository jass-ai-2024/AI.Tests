# не должно пройти в докере

import requests

def get_website_status(url):
    response = requests.get(url)
    return response.status_code

