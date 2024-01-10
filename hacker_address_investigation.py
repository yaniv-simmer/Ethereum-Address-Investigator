import requests
import csv
from typing import List, Tuple

class HackerInvestigator:
    """
    A class dedicated to investigating Ethereum blockchain transactions associated with a specified hacker address.
    """
    def __init__(self, api_key: str ):
        self.api_endpoint: str = "https://api.etherscan.io/api"
        self.api_key: str = api_key
        self.hacker_address: str = '0x0a5984f86200415894821bfefc1c1de036dbf9e7'

    def fetch_hacker_transactions(self) -> List[Tuple[str, str, str]]:
        """
        Fetches transactions associated with the hacker's address from the Ethereum blockchain.
        """

        # Prepare the API request
        params = {
            'module': 'account',
            'action': 'txlist',
            'address': self.hacker_address,
            'startblock': 0,
            'endblock': 99999999,
            'sort': 'asc',
            'apikey': self.api_key
        }
        response = requests.get(self.api_endpoint, params=params)
        data = response.json()

        # Extract the required information from the response
        transactions = [(tx['hash'], tx['from'], tx['to'])for tx in data['result']]
        return transactions

    def write_transactions_to_csv(self) -> None:
        """
        Writes the hacker's transactions to a CSV file.
        """
        transactions = self.fetch_hacker_transactions()

        with open('hacker_investigation.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Attack Transaction Hashes", "Victim Addresses", "Attacker Addresses"])
            writer.writerows(transactions)
