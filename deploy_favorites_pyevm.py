import boa
# from boa.contracts.vyper.vyper_contract import VyperContract

def main():
    print("Let's read in the Vyper code and deploy it!")
    favorites_contract = boa.load("favorites.vy")
    # favorites_contract: VyperContract = boa.load("favorites.vy") --- This is saying favorites_contract of type VyperContract
    # print(type(favorites_contract))
    
    starting_favorite_number = favorites_contract.retrieve() # Retrieve function is a view function so no tx sent
    print(f"The starting favorite number is: {starting_favorite_number}")

    favorites_contract.store(5) # Store function is changing state therefore it sends a transaction
    ending_favorite_number = favorites_contract.retrieve()
    print(f"The ending favorite number is: {ending_favorite_number}")

if __name__ == "__main__":
    main()