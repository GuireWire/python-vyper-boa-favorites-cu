import boa
from vyper import compile_code
from dotenv import load_dotenv
from boa.network import NetworkEnv, EthereumRPC
from web3 import Web3
import os
from eth_account import Account
from encrypt_key import KEYSTORE_PATH, decrypt_key
from getpass import getpass

load_dotenv()

RPC_URL = os.getenv("TENDERLY_RPC_URL")

def main():
    
    print("Let's read in the Vyper code and deploy it!")
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    with open("workshop.vy", "r") as workshop_file:
        workshop_code = workshop_file.read()
        compilation_details = compile_code(workshop_code, output_formats=["bytecode", "abi"])

    chain_id = 111551115 # Make sure this matches your virtual or anvil chain

    print("Getting environment variables...")
    my_address = os.getenv("MY_TENDERLY_ADDRESS")

    # private_key = os.getenv("PRIVATE_KEY")
    private_key = decrypt_key(KEYSTORE_PATH)

    # Create the contract in Python
    workshop_contract = w3.eth.contract(abi=compilation_details["abi"], bytecode=compilation_details["bytecode"])
    # print(favorites_contract)
    # breakpoint()
    
    # Submit the transaction that deploys the contract
    nonce = w3.eth.get_transaction_count(my_address)

    print("Building the transaction...")
    transaction = workshop_contract.constructor().build_transaction(
        { 
            "chainId": chain_id,
            "gas": 3000000,  # Explicit gas limit
            "gasPrice": w3.eth.gas_price,
            # "gasPrice": 1
            "from": my_address,
            "nonce": nonce, }
    )
    print("Signing transaction...")
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    print("We signed it, check it out:")
    print(signed_txn)

    print("Deploying Contract!")
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print("Waiting for transaction to finish...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

def decrypt_key(keystore_path: str) -> str:
    with open(keystore_path, "r") as fp:
        encrypted_account = fp.read()
        password = getpass("Enter your password for your keystore.json:\n")
        key = Account.decrypt(encrypted_account, password)
        print("Decrypted key!")
        return key

# def main():
#     # Set RPC URL
#     rpc = os.getenv("TENDERLY_RPC_URL")
#     # print(rpc)
#     env = NetworkEnv(EthereumRPC(rpc))
#     boa.set_env(env)

#     # Add account
#     my_address = os.getenv("MY_TENDERLY_ADDRESS")
#     private_key = decrypt_key(KEYSTORE_PATH)
#     my_account = Account.from_key(private_key)
#     boa.env.add_account(my_account, force_eoa=True)

#     # Deploy contract
#     workshop_contract = boa.load("workshop.vy")

    # Interact
    starting_my_bool = workshop_contract.get_bool()
    print(f"The starting my bool is: {starting_my_bool}")
    
    print("Setting bool....")
    workshop_contract.set_bool(False)

    ending_my_bool = workshop_contract.get_bool()
    print(f"The ending bool is: {ending_my_bool}")

    # Interact with Add Person function
    print("Storing a person...")
    workshop_contract.add_person("Bob", True)

    person_data = workshop_contract.list_of_people(0)
    print(person_data)

if __name__ == "__main__":
    main()