from sanctioned_addresses_extraction import SanctionsExtractor
from hacker_address_investigation import HackerInvestigator
import argparse

def main(etherscan_api_key: str, infura_api_key: str) -> None:
 

    # ----Assinment 1: Investigate the hacker addresses

    investigator = HackerInvestigator(etherscan_api_key)
    investigator.write_transactions_to_csv()


    # ----Assinment 2: Extract the sanctioned addresses

    extractor = SanctionsExtractor(etherscan_api_key, infura_api_key)
    extractor.fetch_sanctioned_addresses_via_rpc()
    #extractor.fetch_sanctioned_addresses_via_api() # uncomment this line to use the API instead of RPC
    extractor.write_sanctioned_addresses_to_csv()



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-EtherscanApiKey', required=True)
    parser.add_argument('-infuraApiKey', required=True)
    args = parser.parse_args()
    main(args.EtherscanApiKey, args.infuraApiKey)