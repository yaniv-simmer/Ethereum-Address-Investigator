import requests
import csv
from typing import List, Dict
from web3 import Web3
import json

class SanctionsExtractor:
    """
    A class to extract sanctioned Ethereum addresses from a specified smart contract.
    """
    
    ETHERSCAN_API_ENDPOINT = "https://api.etherscan.io/api"
    INFURA_API_ENDPOINT = "https://mainnet.infura.io/v3/"
    CONTRACT_ADDRESS = "0x40C57923924B5c5c5455c48D93317139ADDaC8fb"
    SANCTIONED_ADDRESSES_ADDED_TOPIC = '0x2596d7dd6966c5673f9c06ddb0564c4f0e6d8d206ea075b83ad9ddd71a4fb927'

    def __init__(self, etherscan_api_key: str, infura_api_key: str):
        """
        Initialize the SanctionsExtractor class with API keys.
        """
        self.etherscan_api_key = etherscan_api_key
        self.infura_api_key = infura_api_key
        self.sanctioned_addresses = None

    def get_sanctioned_addresses_via_rpc(self) -> None:
        """
        Fetch sanctioned addresses from the contract using RPC calls.
        """
       
        contract_address = Web3.to_checksum_address(self.CONTRACT_ADDRESS)
        
        # Get the contract ABI
        response = requests.get(self.ETHERSCAN_API_ENDPOINT, params={
            "module": "contract",
            "action": "getabi",
            "address": self.CONTRACT_ADDRESS,
            "apikey": self.etherscan_api_key
        })      
        contract_abi = json.loads(response.json()['result'])

        # Setup Web3 connection and contract instance
        w3 = Web3(Web3.HTTPProvider(self.INFURA_API_ENDPOINT + self.infura_api_key))
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        
        # Define event filter for the SanctionedAddressesAdded event        
        event_filter = contract.events.SanctionedAddressesAdded.create_filter(fromBlock='earliest')
         
        # Get all entries from the event,and process the event data
        events = event_filter.get_all_entries()
        added_sanctioned_addresses = []
        for event in events:
            added_sanctioned_addresses.extend(event.args.addrs) 
        
        # check if the addresses were removed
        renoved_event_filter = contract.events.SanctionedAddressesRemoved.create_filter(fromBlock='earliest')
        removed_events = renoved_event_filter.get_all_entries()
        for event in removed_events:
            if event.args.addrs in added_sanctioned_addresses:
                added_sanctioned_addresses.remove(event.args.addrs)
        
        # Now `sanctioned_addresses` contains all addresses from the SanctionedAddressesAdded events
        self.sanctioned_addresses = list(set(added_sanctioned_addresses)) # remove duplicates
    

    def write_sanctioned_addresses_to_csv(self) -> None:
        """
        Write the fetched sanctioned addresses to a CSV file.
        """

        with open('sanctioned_addresses.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Sanctioned Addresses"])
            for address in self.sanctioned_addresses:
                writer.writerow([address])
        

    def get_sanctioned_addresses_via_api(self) -> None:
        """
        Fetch the sanctioned addresses from the Ethereum contract using the Etherscan API.
        """
        
        payload = {
            "module": "logs",
            "action": "getLogs",
            "address": self.CONTRACT_ADDRESS,
            "topic0": self.SANCTIONED_ADDRESSES_ADDED_TOPIC,
            "startblock": 0,
            "endblock": 99999999,
            "sort": "asc",
            "apikey": self.etherscan_api_key
        }
        response = requests.get(self.ETHERSCAN_API_ENDPOINT, params=payload)
        data = response.json()

        # Extract the sanctioned addresses   
        self.sanctioned_addresses = self.decode_ethereum_addresses(data['result'])

    def decode_ethereum_addresses(self, hex_string_lst: List[Dict[str, str]]) -> List[str]:
        """
        Decode Ethereum addresses from a list of hexadecimal strings.

        Args:
            hex_string_lst (List[Dict[str, str]]): List of hexadecimal string dictionaries.

        Returns:
            List[str]: List of decoded Ethereum addresses.
        """
        addresses = []
        for hex_string in hex_string_lst:
            relevant_part = hex_string['data'][130:]  # Extract relevant part of the data
            for i in range(24, len(relevant_part), 64):
                address = relevant_part[i:i+40]
                addresses.append('0x' + address)
        return list(set(addresses)) # remove duplicates
