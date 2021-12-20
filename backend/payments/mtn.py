import requests
import logging
import uuid
import base64


logger = logging.getLogger(__name__)


class MTNAPI(object):
    def __init__(self, sub_key, api_key=None, user_id=None, url=None, callback=None):
        self.SUBSCRIPTION_KEY = sub_key
        self.API_KEY = api_key
        self.USER_ID = user_id
        self.URL = url
        self.CALLBACK = callback

        if not self.USER_ID:
            self.USER_ID = str(uuid.uuid4())

    def sandbox_user(self):
        headers = {
            "X-Reference-Id": self.USER_ID,
            "Ocp-Apim-Subscription-Key": self.SUBSCRIPTION_KEY,
            "Content-Type": "application/json"
        }
        return requests.post(
            f"{self.URL}/v1_0/apiuser",
            headers=headers,
            json={"providerCallbackHost": self.CALLBACK}
        )

    def sandbox_keys(self):
        headers = {
            "X-Reference-Id": self.USER_ID,
            "Ocp-Apim-Subscription-Key": self.SUBSCRIPTION_KEY,
            "Content-Type": "application/json"
        }

        reply = requests.post(
            f"{self.URL}/v1_0/apiuser/{self.USER_ID}/apikey",
            headers=headers
        )

        if reply.status_code == 201:
            self.API_KEY = reply.json()["apiKey"]

        return reply

    def token(self):
        if not all([self.API_KEY, self.USER_ID]):
            logger.error("UserId or APIKey is empty!")
            return

        auth_str = f"{self.USER_ID}:{self.API_KEY}".encode()
        authorization = base64.b64encode(auth_str).decode()

        headers = {
            "Authorization": f"Basic {authorization}",
            "Ocp-Apim-Subscription-Key": self.SUBSCRIPTION_KEY,
            "Content-Type": "application/json"
        }

        reply = requests.post(
            f"{self.URL}/disbursement/token/",
            headers=headers
        )
        return reply

    def _get_token(self):
        reply = self.token()
        if reply.status_code != 200:
            return None
        else:
            return reply.json()["access_token"]
        
    def balance(self):
        token = self._get_token()
        if not token:
            logger.error("Token is missing!")
            return

        headers = {
            "Authorization": f"Bearer {token}",
            "X-Target-Environment": "sandbox",
            "Ocp-Apim-Subscription-Key": self.SUBSCRIPTION_KEY,
            "Content-Type": "application/json"
        }

        return requests.get(
            f"{self.URL}/disbursement/v1_0/account/balance",
            headers=headers
        )

    def transfer(self, amount, receiver, reference):
        token = self._get_token()
        if not token:
            logger.error("Token is missing!")
            return

        headers = {
            "Authorization": f"Bearer {token}",
            "X-Target-Environment": "sandbox",
            "Ocp-Apim-Subscription-Key": self.SUBSCRIPTION_KEY,
            "Content-Type": "application/json",
            "X-Reference-Id": reference
        }

        data = {
            "amount": amount,
            "currency": "EUR",
            "externalId": reference,
            "payee": {
                "partyIdType": "MSISDN",
                "partyId": receiver
            },
            "payerMessage": "Test",
            "payeeNote": "Test"
        }

        return requests.post(
            f"{self.URL}/disbursement/v1_0/transfer",
            headers=headers,
            json=data
        )

    def get_transfer_status(self, reference):
        token = self._get_token()
        if not token:
            logger.error("Token is missing!")
            return

        headers = {
            "Authorization": f"Bearer {token}",
            "X-Target-Environment": "sandbox",
            "Ocp-Apim-Subscription-Key": self.SUBSCRIPTION_KEY,
            "Content-Type": "application/json"
        }

        return requests.get(
            f"{self.URL}/disbursement/v1_0/transfer/{reference}",
            headers=headers
        )
        