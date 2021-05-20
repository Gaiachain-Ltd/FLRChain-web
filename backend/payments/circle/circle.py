import requests
import json


class CircleAPI(object):
    def __init__(self, key, enviroment_url):
        self.API_KEY = key
        self.ENVIROMENT_URL = enviroment_url

    def request(self, type, url, data=None):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.API_KEY}"
        }

        return requests.request(type, url, headers=headers, data=data)

    def get_public_key(self):
        url = f"{self.ENVIROMENT_URL}/v1/encryption/public"

        reply = self.request("GET", url)

        if reply.status_code == 200:
            return reply.json()
        else:
            return None

    def save_card(self, data):
        pass