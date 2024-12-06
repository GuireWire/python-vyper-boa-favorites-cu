from eth_account import Account
from getpass import getpass
from pathlib import Path
import json

KEYSTORE_PATH = Path(".keystore.json")

def decrypt_key(keystore_path: Path) -> str:
    """Decrypt the private key from the keystore file."""
    # Get the password to decrypt the keystore
    password = getpass("Enter your password:\n")  # Use getpass.getpass() correctly
    
    # Load the encrypted keystore data
    with keystore_path.open("r") as fp:
        encrypted_account = json.load(fp)

    # Decrypt the account using the provided password
    private_key = Account.decrypt(encrypted_account, password)
    
    return private_key

def main():
    # input for your private key
    private_key = getpass.getpass("Enter your private key:\n")
    my_account = Account.from_key(private_key)

    password = getpass.getpass("Enter a password:\n")
    encrypted_account = my_account.encrypt(password)

    print(f"Saving to {KEYSTORE_PATH}...")
    with KEYSTORE_PATH.open("w") as fp:
        json.dump(encrypted_account, fp)


if __name__ == "__main__":
    main()