import os
import boa
from dotenv import load_dotenv
from boa.network import NetworkEnv, EthereumRPC
from eth_account import Account

MY_CONTRACT = "0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9"

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

    # Load contract
    workshop_deployer = boa.load_partial("workshop.vy")
    workshop_contract = workshop_deployer.at(MY_CONTRACT)
    
    # Interact
    my_bool = workshop_contract.get_bool()
    print(f"My bool is: {my_bool}")

    # Update
    workshop_contract.set_bool(False)
    my_bool_updated = workshop_contract.get_bool()
    print(f"The updated bool is: {my_bool_updated}")

if __name__ == "__main__":
    main()