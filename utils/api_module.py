#!/usr/bin/python3
import configparser
import json
import requests
from requests import RequestException, ConnectionError, Timeout
from web3 import Web3, HTTPProvider
from ethtoken.abi import EIP20_ABI

config = configparser.ConfigParser()
config.read('config.ini')
index_api_url       = f'{config["default"]["index_api_url"]}/api'
tbtc_contract_addr  = Web3.toChecksumAddress(config["default"]["tbtc_contract"])
eth_provider        = config["default"]["eth_rpc_provider"]
w3                  = Web3(HTTPProvider(eth_provider))

with open("utils/tbtc_abi.json") as f:
    info_json = json.load(f)
abi = info_json
contract = w3.eth.contract(tbtc_contract_addr, abi=abi)


def tdt_id_by_lot_size(lot_size_):
    get_tdt_id_url = f"{index_api_url}/op/tdt_id?lot={lot_size_}&token=TBTC"
    try:
        req = requests.get(get_tdt_id_url)
        if req.status_code == 200 and req.text[0:2] == "0x" and len(req.text) == 42:
            print(req.text)
            return req.text

        else:
            print(req.text)
            return "Can't find a suitable TDT_ID for current lot size"

    except (RequestException, ConnectionError, Timeout, Exception) as connectErr:
        print(f'Error in tdt_id_by_lot_size():\n{connectErr}')
        return "error"


def tbtc_total_supply():
    try:
        supply_ = contract.functions.totalSupply().call()
        return supply_ / 1e18

    except Exception as supplyErr:
        print(supplyErr)
        return "error"
