# Ethereum Hacker Investigation 

## Overview
- <ins>**Assignment 1.</ins> Hacker Address Investigation.py:**\
 Investigate Ethereum addresses using the Etherscan API.


- <ins>**Assignment 2.</ins> Sanctioned Addresses Extraction.py:**\
 Extract  Ethereum addresse from a Chainalysis oracle contract usind the **Infura API** and **<ins>optionally</ins> the Etherscan API**. please note in the code the functions :
    - fetch_sanctioned_addresses_via_api()
    - fetch_sanctioned_addresses_via_rpc()

<br />-built with Python 3.10.11

## Installation and Usage
1. Before running the scripts, ensure that [Python 3](https://www.python.org/downloads/) is installed on your machine.\
install the necessary libraries using pip:

```bash
pip install requests web3 argparse
```


2. clone the repository with the following command:

```bash
git clone https://github.com/yaniv-simmer/Ethereum-Address-Investigator.git
```


3. To run the script, you need to provide your [Etherscan API](https://docs.etherscan.io/getting-started/viewing-api-usage-statistics) key and [Infura API key](https://docs.infura.io/getting-started).\
Use the following command:

```bash
python main.py -EtherscanApiKey <YOUR_ETHERSCAN_API_KEY> -infuraApiKey <YOUR_INFURA_API_KEY>
```




## Output
- **Hacker Investigation**: `hacker_investigation.csv` containing transaction hashes, victim addresses, and attacker addresses.
- **Sanctioned Addresses**: `sanctioned_addresses.csv` containing a list of sanctioned Ethereum addresses.


## License


This project is licensed under the [MIT License](LICENSE).




