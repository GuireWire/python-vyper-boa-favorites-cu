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
    workshop_contract = boa.load("workshop.vy")

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