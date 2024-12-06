import boa
from dotenv import load_dotenv
from boa.network import NetworkEnv, EthereumRPC
import os
from eth_account import Account

load_dotenv()

def main():
    # Set RPC URL
    rpc = os.getenv("RPC_URL")
    # print(rpc)
    env = NetworkEnv(EthereumRPC(rpc))
    boa.set_env(env)

    # Add account
    anvil_private_key = os.getenv("ANVIL_PRIVATE_KEY")
    my_account = Account.from_key(anvil_private_key)
    boa.env.add_account(my_account, force_eoa=True)

    # Deploy contract
    favorites_contract = boa.load("favorites.vy")

    # Interact
    starting_favorite_number = favorites_contract.retrieve()
    print(f"The starting favorite number is: {starting_favorite_number}")
    
    print("Storing number....")
    favorites_contract.store(5)

    ending_favorite_number = favorites_contract.retrieve()
    print(f"The ending favorite number is: {ending_favorite_number}")

    # Interact with Add Person function
    print("Storing a person...")
    favorites_contract.add_person("Bob", 11)

    person_data = favorites_contract.list_of_people(0)
    print(person_data)

if __name__ == "__main__":
    main()