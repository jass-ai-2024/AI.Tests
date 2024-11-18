# не должно пройти в докере

import requests

def get_website_status(url):
    response = requests.get(url)
    return response.status_code

if __name__ == "__main__":
    print(get_website_status("https://example.com"))
