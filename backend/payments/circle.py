import requests
import json
import logging


logger = logging.getLogger(__name__)


class CircleAPI(object):
    def __init__(self, key, enviroment_url):
        self.API_KEY = key
        self.ENVIROMENT_URL = enviroment_url

    def request(self, type, url, data=None):
        headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Authorization": f"Bearer {self.API_KEY}",
        }

        reply = requests.request(type, url, headers=headers, json=data)

        if reply.status_code in [200, 201]:
            return reply.json()
        else:
            logger.error("Invalid response: %s %s", reply.status_code, reply.json())
            return None

    def get_public_key(self):
        url = f"{self.ENVIROMENT_URL}/v1/encryption/public"
        return self.request("GET", url)

    def save_card(self, data):
        url = f"{self.ENVIROMENT_URL}/v1/cards"
        return self.request("POST", url, data)

    def create_payment(self, data):
        url = f"{self.ENVIROMENT_URL}/v1/payments"
        return self.request("POST", url, data)

    def payment_info(self, payment_id):
        url = f"{self.ENVIROMENT_URL}/v1/payments/{payment_id}"
        return self.request("GET", url)

    def transfer_usdc(self, data):
        url = f"{self.ENVIROMENT_URL}/v1/transfers"
        return self.request("POST", url, data)

    def transfer_info(self, transfer_id):
        url = f"{self.ENVIROMENT_URL}/v1/transfers/{transfer_id}"
        return self.request("GET", url)