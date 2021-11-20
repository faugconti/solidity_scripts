import os
from web3 import Web3
import json
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

load_dotenv()

install_solc("0.6.0")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)


compiled_sol = compile_standard({
    'language': 'Solidity',
    'sources': {'SimpleStorage.sol': {'content': simple_storage_file}},
    'settings': {
        'outputSelection': {
            '*': {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
        }
    },
}, solc_version="0.6.0")

# print(compiled_sol)

with open('compiled_code.json', 'w') as file:
    json.dump(compiled_sol, file)

# get bytecode

bytecode = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['evm']['bytecode']['object']

# get abi

abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']
# print(abi)

# for connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0xAECc5E9C7263dB77E1076b1C4015946aB2F0d894"
#private_key = "0xd257e0bb8d5d416e6302bd0bed8fab27c693a67c812e099975d910fa6614660d"
private_key = os.getenv("PRIVATE_KEY")

# create the contract in python

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)


# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {'chainId': chain_id, 'from': my_address, "nonce": nonce})

signed_txn = w3.eth.account.sign_transaction(
    transaction, private_key=private_key)

print("Deploying contract...")

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Contract Deplyed!")

# working with the contract , you always need
# contract address + contract abi

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call -> Simulate making the call and getting a return value
# Transact -> actually make a state change

print(simple_storage.functions.retrieve().call())

print("Updating contract...")

store_transaction = simple_storage.functions.store(15).buildTransaction({
    "chainId": chain_id,
    "from": my_address, "nonce": nonce+1
})
signed_store_tx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key)

send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Contract updated!...")
print(simple_storage.functions.retrieve().call())
