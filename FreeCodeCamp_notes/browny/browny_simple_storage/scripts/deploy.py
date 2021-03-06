from brownie import accounts, network, config, SimpleStorage
import os


def deploy_simple_storage():
    account = get_account()
    print(account)
    # account = accounts.load("freecodecamp-account")
    # print(account)  # private key

    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # print(account)
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)

    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    print(stored_value)
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    updated_store_value = simple_storage.retrieve()
    print(updated_store_value)


def get_account():
    if network.show_active() == 'development':
        return accounts[0]
    else:
        return accounts.add(config['wallets']["from_key"])


def main():
    deploy_simple_storage()
