# %% [markdown]
# # MACoin Blockchain

# %% [markdown]
# ## Import Section

# %%
# import necessary libraries

import subprocess
import sys
# Function to install a package using pip
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
# List of required libraries
required_libraries = [
    'hashlib',
    'datetime',
    'secrets',
    'pandas',
    'IPython.display',
    'requests',
    'matplotlib',
    'yfinance',
    'graphviz']
# Dictionary to map module names to pip install names (for modules where they differ)
pip_names = {
    'IPython.display': 'ipython',
    'matplotlib': 'matplotlib',
    'pandas': 'pandas',
    'requests': 'requests',
    'yfinance': 'yfinance',
    'graphviz': 'graphviz',}
# Check and install missing libraries
for lib in required_libraries:
    try:
        exec(f"import {lib.split('.')[0]}")
        print(f"{lib} is already installed.")
    except ImportError:
        print(f"{lib} not found. Installing...")
        install(pip_names.get(lib, lib.split('.')[0]))
# Now import all libraries (this ensures they are available for use)
import hashlib
import datetime
import secrets
import pandas as pd
from IPython.display import display, HTML
import requests
import matplotlib.pyplot as plt
import yfinance as yf
from graphviz import Digraph

# %% [markdown]
# ## Code Section

# %%
############################################################################################
####################################### Wallet Class #######################################
############################################################################################

# Individual wallets
class Wallet:
    def __init__(self, address, password, phrase, creation_date, starting_balance=0): # Initialize wallet with address, password, recovery phrase, creation date, and starting balance
        self.address = address
        self.balance = starting_balance
        self.password = password
        self.phrase = phrase
        self.creation_date = creation_date 


    # Add amount to wallet balance
    def add_amount(self, amount):
        self.balance += float(amount)


    # Deduct amount from wallet balance
    def deduct_amount(self, amount): 
        if self.balance >= float(amount):
            self.balance -= float(amount)
        else: # retun error message if balance not high enough
            raise ValueError("Insufficient balance.")



############################################################################################
####################################### Block Class ########################################
############################################################################################
# Class for individual blocks on the chain, containing a timestamp, data, and the previous block's hash value
# --> One block will contain one transaction, and will be mined immediately upon execution
class Block:
    def __init__(self, timestamp, data, previous_hash): # Initialize block with timestamp, data, and previous block's hash
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.transaction = [] # Transaction details will be stored here
        self.hash = self.calculate_hash() # Hash value of the block


    # Calculate a block's hash value: hexadecimal SHA256 hash of the concatenated contents
    def calculate_hash(self):
        hash_string = str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.transaction) # Concatenate block contents
        return hashlib.sha256(hash_string.encode()).hexdigest() # Return hexadecimal SHA256 hash of the concatenated contents



############################################################################################
################################### SMART CONTRACT Class ###################################
############################################################################################
# Class for smart contracts, containing the contract address, contract name, conditions, and contract type
class smart_contract:
    # Initialize smart contract with address, contract name, conditions, and contract type
    def __init__(self, address=None, contract_name=None, conditions=None, contract_type=None):
        self.address = address
        self.contract_name = contract_name
        self.conditions = conditions
        self.contract_type = contract_type


    # show terms and conditions of standardized contract
    def show_SC_terms(self):
        # function that shows the terms and conditions of the contract
        funding = ["When wallet [address] reaches [amount_total] then send [amount_indiv] to [receiver]"] # Standard terms for funding contracts
        transaction = ["When wallet [address_A] transfers [amount_total] to [address_B] then I send [amount_indiv] to [receiver]"] # Standard terms for transaction contracts
        standard_terms = [funding, transaction]
        print(f"Standard terms for funding contracts: {funding}\n", "Standard terms for transaction contracts: {transaction}")


    # explanation of conditions of standardized smart contract
    def explain_conditions(self):
        print("Depending on the type of contract, the conditions will be different. This is generally based on the type of contract.\n",
              "The allowed contract types are: funding, transaction, other. If the selected type does not match one of these, it is automatically categoriezed as 'other'.\n",
              "Contracts of type 'other' will not be executed automatically, but will need to be checked manually and do not have the blockchain execution.\n",
              "If the contract is of type 'funding', the conditions will be based on the funding goal. The conditions should follow a certain pattern, precisely, based on the following:\n",
              "'When wallet [address] reaches [amount_total] then send [amount_indiv] to [receiver]'.\n",
              "If the contract is of type 'transaction', the conditions will be based on other transactions. The conditions should follow a certain pattern, precisely, based on the following:\n",
              "'When wallet [address_A] transfers [amount_total] to [address_B] then I send [amount_indiv] to [receiver]'.\n",
              "For these two types of contract, the blockchain will automatically check and execute the contract if the conditions are met.\n",
              "If different, less restrictive conditions are needed, the contract must be of type 'other', where less restrictive conditions can be implemented.\n")



############################################################################################
##################################### Blockchain Class #####################################
############################################################################################
# Will only be initialized once and will be updated as new blocks are added
class Blockchain:
    # Creates the first ("genesis") block, a dictionary of registered wallets, a list of transactions, and data storage for smart contracts
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.wallets = {}
        self.SC = {}
        self.contract_parties = {}
        self.SCconditions = {}
        self.SCtypes = {}
        self.starting_balance = 100.0


    # Create the first block in the chain, with a hash value =0
    def create_genesis_block(self):
        return Block(datetime.datetime.now(), "Genesis Block", "0")


    # Function to authenticate user
    def authenticate_user(self, address=None, password=None):
        # Check if address and password are provided, otherwise prompt user for input
        if not address: # If address is not provided, ask user for address
            for i in range(3):
                address = input("Enter your wallet address: ")
                if address in self.wallets: # Check if wallet exists
                    if password != None and self.wallets[address].password == password: # Check if password is correct if a password is provided
                        return True
                    break
                else:
                    print("Erro. Wallet not found.") # Return error if wallet provided was not found, and prompt user to try again

        # checks if password is provided otherwise asks user for password and checks if password is correct
        if not password: # If password is not provided, ask user for password
            for i in range(3):
                password = input("Enter the password for your wallet: ")
                if self.wallets[address].password == password: # Check if password is correct
                    return True
                else:
                    print("Error. Incorrect password.") # Return error if password provided was incorrect, and prompt user to try again

        # checks if address and password are provided and checks if wallet exists and password is correct
        if address in self.wallets and self.wallets[address].password == password:
            return True

        # if none of the above conditions are met, raises an error
        else:
            raise ValueError("Error. Wallet not found or incorrect password.")       


    # Add a new block to the chain, including timestamp, data, transaction, and previous block's hash
    def add_block(self, transaction, data):
        previous_block = self.chain[-1]
        new_block = Block(datetime.datetime.now(), data, previous_block.hash)
        new_block.transaction = transaction
        self.chain.append(new_block)
        self.execute_contract() # Automatically execute smart contracts after each block is added


    # Create a new wallet registered to the blockchain
    def create_wallet(self, testing=False):
        if not testing: # If not in testing mode, prompt user for input
            # Prompts user to enter a password for the wallet
            password = input("Enter a password for your wallet: ")

        if testing: # If in testing mode, set password to None (only for testing purposes, would be removed in production version)
            password = None

        # Random words for the recovery phrase, consisting of 100 words
        words = [
            'after', 'air', 'always', 'angry', 'apple', 'bad', 'ball', 'banana', 'bed', 'before',
            'big', 'bird', 'book', 'car', 'cat', 'choices', 'close', 'cold', 'cry', 'day',
            'dog', 'drink', 'early', 'earth', 'eat', 'excuse', 'family', 'fast', 'feel', 'fire',
            'first', 'fish', 'food', 'friend', 'good', 'goodbye', 'happy', 'hat', 'hate', 'hear',
            'hello', 'help', 'here', 'hot', 'house', 'hungry', 'jump', 'last', 'late', 'laugh',
            'learn', 'love', 'luck', 'maybe', 'month', 'moon', 'never', 'new', 'next', 'night',
            'no', 'now', 'old', 'open', 'options', 'play', 'please', 'run', 'sad', 'see',
            'sit', 'sleep', 'slow', 'small', 'smile', 'soon', 'sorry', 'stand', 'star', 'start',
            'stop', 'sun', 'talk', 'thank', 'then', 'there', 'thirsty', 'time', 'tired', 'touch',
            'tree', 'walk', 'water', 'week', 'welcome', 'work', 'year', 'yes', 'you', 'young']
        
        # Set initial wallet_created tag to False
        wallet_created = False
        
        # Finds a 5-byte hexadecimal address that is not yet in use, registers the wallet instance to wallet dictionary
        for i in range(5):
            address = secrets.token_hex(5) # 5-byte hexadecimal address
            if address in self.wallets: # If address already in use, skip
                continue
            else:
                creation_date = datetime.datetime.now() # Get current date and time
                phrase = " ".join([secrets.choice(words) for i in range(12)]) # 12-word recovery phrase
                self.wallets[address] = Wallet(address, password, phrase, creation_date, self.starting_balance) # Register wallet to wallet dictionary
                print(f"This is your wallet's address: '{address}'.\nThis is your recovery phrase: {phrase}")
                wallet_created = True # Set wallet_created tag to True
                break
        
        # Return error if wallet was not created
        if not wallet_created:
            raise ValueError("Error. Wallet not created. Please try again.")
        else:
            return address # Return the wallet address (for ease of testing)
        
    
    # Function to change wallet password
    def change_password(self, address):
        if self.authenticate_user(address): # Check if user is authenticated
            self.wallets[address].password = input("Enter a new password:") # Prompt user for new password
            print("Password changed successfully.")
        else: # Return error if user is not authenticated
            raise ValueError("Error. Unable to change password.")
        
    
    # Function to recover wallet using recovery phrase
    def recover_wallet(self, address):
        if address in self.wallets: # Check if wallet exists
            recovery_phrase = input("Enter your recovery phrase: ") # Prompt user for recovery phrase    
            if recovery_phrase == self.wallets[address].phrase: # Check if recovery phrase is correct
                password = input("Wallet recovered successfully. Enter new password: ") # Prompt user for new password
                self.wallets[address].password = password # Set new password
                print("Password reset successfully.")
            else: # Return error if recovery phrase is incorrect
                raise ValueError("Error. Incorrect recovery phrase.")
        else: # Return error if wallet does not exist
            raise ValueError("Error. Wallet not found. Please try again.")
    
    
    # Function to enable user to delete their wallet
    def delete_wallet(self, address):
        if self.authenticate_user(address): # Check if user is authenticated
            for i in range(3): # Allow 3 attempts
                answer = input(f"Are you sure you want to delete wallet {address}? (yes/no): ") # Prompt user for confirmation
                if answer.lower() == "yes": # If user confirms, delete wallet
                    del self.wallets[address]
                    print("Wallet deleted.")
                    break
                elif answer.lower() == "no": # If user declines, do not delete wallet
                    print("Wallet not deleted.")
                    break
                else: # Return error if input is invalid
                    print("Invalid input. answer must be 'yes' or 'no'.")
        else: # Return error if user is not authenticated
            raise ValueError("Error. Unable to delete wallet.")


    # Return wallet balance
    def get_wallet_balance(self, address):
        if address in self.wallets: # Check if wallet exists
            return self.wallets[address].balance # Return wallet balance
        else: # Return error if wallet does not exist
            raise ValueError("Error. Wallet not found.")
    

    # Function to transfer coins between wallets, takes sender, receiver addresses, along with amount, data, and sender password as inputs
    def transfer_funds(self, sender, receiver, amount, data, testing=False):
        if not testing: # If not in testing mode, check if user authenticated
            self.authenticate_user(sender) # Check if sender exists and is authenticated

        if receiver in self.wallets: # Check if receiver wallet exists
            sender_wallet = self.wallets[sender]
            receiver_wallet = self.wallets[receiver]
            # Check to see if sender balance is high enough, and if sender password is correct
            if sender_wallet.balance >= amount > 0 and sender_wallet != receiver_wallet: # Check if sender balance is high enough, amount is positive, and sender is not receiver
                # Deduct amount from sender wallet, add to receiver wallet
                sender_wallet.deduct_amount(amount)
                receiver_wallet.add_amount(amount)
                
                # Add the block containing the transaction to the blockchain
                transaction = [sender_wallet.address, receiver_wallet.address, amount, data, datetime.datetime.now()]
                block_data = f"Block {len(self.chain)}" # Block data is the block number
                self.add_block(transaction, block_data) # Add the block to the blockchain
                print("Funds transferred successfully.")
        
        # Error messages for various cases
            elif sender_wallet.balance < amount: # If sender balance is too low
                raise ValueError("Insufficient balance.")
            elif amount <= 0: # If amount is not positive
                raise ValueError("Amount must be positive.")
            elif sender_wallet == receiver_wallet: # If sender and receiver are the same
                raise ValueError("Sender and receiver must be different.")

        elif receiver not in self.wallets: # If receiver wallet does not exist
            raise ValueError("Receiver wallet not found.")
        else:
            raise ValueError("Error. Please try again later.")


    # Basic print chain function: prints contents of all blocks on chain
    def print_chain(self):
        for block in self.chain:
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Transaction: {block.transaction}")
            print(f"Hash: {block.hash}")
            print()

    # Display chain diagram
    def display_chain_diagram(self):
        dot = Digraph(comment='Blockchain', node_attr={'shape': 'box', 'style': 'filled', 'color': 'lightgrey', 'fillcolor': 'lightgrey'}, graph_attr={'rankdir': 'BT'})

        for block in self.chain:
            # Constructing the label using HTML-like syntax without explicit width control
            label_text = f"<<table border='0' cellspacing='0' cellborder='0'><tr><td align='left'><b>Previous Hash: {block.previous_hash}</b></td></tr>"
            if block.previous_hash == "0":  # Only include the timestamp for the genesis block
                label_text += f"<tr><td align='left'>Timestamp: {block.timestamp}</td></tr>"
            label_text += f"<tr><td align='left'>Data: {block.data}</td></tr><tr><td align='left'>Transaction: {block.transaction[:4]}</td></tr></table>>"

            # Add nodes using the block's hash as the identifier, with increased margin to provide more space
            dot.node(block.hash, label=label_text, margin='0.4,0.2')  # Increased left margin for better text fit

            # Add edges from this block to the previous block if it's not the genesis block
            if block.previous_hash != "0":
                dot.edge(block.hash, block.previous_hash)

        display(dot)


    # Function to retrieve the transaction history of a single wallet address
    def get_wallet_transactions(self, wallet_address):
        # Check if the wallet exists
        if wallet_address not in self.wallets:
            print("Wallet not found.")
            return pd.DataFrame()  # Return an empty DataFrame if wallet is not found

        # Initialize a list to store transaction details 
        transactions_list = []

        # Initialize the wallet object
        #wallet = self.wallets[wallet_address]
        
        balance_after_transfer = self.wallets[wallet_address].balance # Set initial balance after transfer to the wallet's current balance

        # Loop through the chain in reverse chronological order
        for index, block in enumerate(reversed(self.chain)):
            transaction = block.transaction
            
            if not transaction or transaction[0][:2]=="SC": # Skip if the block contains no transfer of funds
                continue
            
            # Unpack the transaction details into individual variables
            sender, receiver, amount, data, timestamp = transaction
            
            # Get wallet balance after transaction via reverse calculation (starting with current balance, reverse transactions to get to balance after previous)
            if index > 0: # Skip the most current block since balance after transfer is already set to the current balance
                for i in range(index, 0, -1): # Loop through the more recent blocks to find next transaction, starting with the next block
                    if self.chain[-i].transaction[0][:2] == "SC": # Skip smart contract transactions with no fund transfer
                        continue
                    else:
                        next_sender, next_receiver, next_amount, next_data, next_timestamp = self.chain[-i].transaction # Get the next transaction details
                        if wallet_address in (next_sender, next_receiver): # Check if the wallet is involved in the next transaction
                            balance_after_transfer = balance_after_transfer + next_amount if wallet_address == next_sender else balance_after_transfer - next_amount # Update the balance after transfer for a given row
                        break

            # Determine how the wallet is involved in this transaction
            if wallet_address == sender: # Check if the wallet is the sender
                transaction_type = "Outgoing"
            elif wallet_address == receiver: # Check if the wallet is the receiver
                transaction_type = "Incoming"
            else:
                continue

            # Append transaction details
            transactions_list.append({
                "Block Index": len(self.chain) - 1 - index,
                "Transaction Hash": block.hash,
                "Timestamp": timestamp,
                "Sender": sender,
                "Receiver": receiver,
                "Transaction Type": transaction_type,
                "Amount": float(amount),
                "Balance after Transfer": float(balance_after_transfer),
                "Reference": data})

        # Create a DataFrame from the transactions list
        df = pd.DataFrame(transactions_list)
        if not df.empty:
            # Sort by Block Index in descending order to have the most recent transactions at the top
            df = df.sort_values(by="Block Index", ascending=False).reset_index(drop=True)
    
        return df
    

   # Function to print the transaction history of a single wallet address
    def print_wallet_transactions(self, wallet_address):
        df = self.get_wallet_transactions(wallet_address) # Retrieve the transaction history of the wallet
        if df.empty: # Print error message if no transactions are found
            raise ValueError("No transactions found for this wallet.")
        else: # Display the transaction history in a formatted HTML table
            html_table = df.to_html(index=False, justify='center')
            display(HTML(html_table))
            
    # Function to retrieve an overview of all wallets on the blockchain
    def get_wallets_overview(self):
        # Initialize a list to store wallet summaries
        wallets_list = []

        # Loop through all wallets and collect their details
        for index, (address, wallet) in enumerate(self.wallets.items(), start=1): # Enumerate the wallets with an index starting from 1
            transaction_numbers = len(self.get_wallet_transactions(address)) # Get the number of transactions for each wallet

            # Add wallet summary to the list
            wallets_list.append({
                "#": index,
                "Wallet Address": address,
                "Balance": wallet.balance,
                "Number of Transactions": transaction_numbers,
                "Creation Date": wallet.creation_date
            })
            
            # Create a DataFrame from the wallets list
            df = pd.DataFrame(wallets_list)
            # Sort by Creation Date in ascending order to have the oldest wallets at the top
            df = df.sort_values(by="Creation Date").reset_index(drop=True)

        return df


    # Function to print the overview of all wallets on the blockchain
    def print_wallets_overview(self):
        df = self.get_wallets_overview() # Retrieve the overview of all wallets
        if df.empty: # Print error message if no wallets are found
            raise ValueError("No wallets found.")
        else: # Display the overview in a formatted HTML table
            html_table = df.to_html(index=False, justify='center')
            display(HTML(html_table))


    # Function to retrieve all transactions across all wallets
    def get_all_transactions(self):
        # Initialize a list to store transaction details
        transactions_list = []

        # Loop through all blocks to collect transactions
        for index, block in enumerate(self.chain):
            transaction = block.transaction
            if not transaction or transaction[0][:2]=="SC": # Skip if the block contains no transfer of funds
                continue
    
            # Unpack the transaction details into individual variables
            sender, receiver, amount, data, timestamp = transaction

            # Append transaction details
            transactions_list.append({
                "Block Index": index,
                "Transaction Hash": block.hash,
                "Timestamp": timestamp,
                "Sender": sender,
                "Receiver": receiver,
                "Amount": float(amount),
                "Reference": data
            })

        # Create a DataFrame from the transactions list
        df = pd.DataFrame(transactions_list)
        if not df.empty:
            # Sort by Timestamp in descending order to have the most recent transactions at the top
            df = df.sort_values(by="Timestamp", ascending=False).reset_index(drop=True)

        return df

    # Function to print all transactions across all wallets
    def print_all_transactions(self):
        df = self.get_all_transactions() # Retrieve all transactions
        if df.empty: # Print error message if no transactions are found
            raise ValueError("No transactions found.")
        else: # Display the transactions in a formatted HTML table
            html_table = df.to_html(index=False, justify='center')
            display(HTML(html_table))


##############################
### SMART CONTRACT SECTION ###
##############################
    # Function to create a smart contract
    def create_SC(self, address, conditions=None, contract_type=None, testing=False):
        # function that initiates the process of creating a smart contract
        if testing or self.authenticate_user(address): # checks to authenticate user unless in testing mode
            for i in range(5):
                contract_name = "SC" + secrets.token_hex(5) # Generate a 5-byte hexadecimal contract name
                if contract_name in self.SC: # ensures that the contract name does not already exist
                    continue
                else: # creates the contract
                    contract = self.create_contract(address, contract_name, conditions, contract_type, testing)    
                    if contract != False and contract != None: # ensures the contract is created successfully
                        # stores the contract, conditions, and contract type
                        #self.SC[contract_name] = contract
                        #self.SCconditions[contract_name] = conditions
                        #self.SCtypes[contract_name] = contract_type
                        print(f"Smart Contract {contract_name} created successfully.")
                    break
        else: # returns an error if the user is not authenticated
            raise ValueError("Error. Could not create contract. Please try again later.")


    # creates contract
    def create_contract(self, address, contract_name, conditions, contract_type, testing):
        # function that creates a contract based on the conditions and contract type specified
        allowed_contract_types = ["funding", "transaction", "other"] # standardized contract types compatible with the blockchain
        # checking conditions
        if conditions == None:
            conditions, contract_type = self.conditions() # checks if conditions are specified, otherwise prompts user to specify them
        
        elif not isinstance(conditions, list): # checks if conditions are in list format
            print("Conditions could not be automated. Please check execution of contract manually.")
            conditions = [conditions] # converts conditions to list format
            contract_type = "other" # sets contract type to 'other' as conditions could not be automated

        elif contract_type in allowed_contract_types: # checks if contract type is in allowed contract types
            # does not check whether the conditions in the list fit into the selected contract type
            # Assumption that conditions and contract types are correct
            conditions = conditions
            contract_type = contract_type
        
        else: # if contract type is not in allowed contract types, sets contract type to 'other'
            contract_type = "other"
            print("Contract type not recognized. Defaulting to type 'other'. See explanation for details.")
            choice = input("Do you want to see the explanation of the contract types? (yes/no): ") # asks user if they want to see the explanation of the contract types
            if choice.lower() == "yes":
                smart_contract.explain_conditions() # shows the explanation of standardized contract types
        
        contract = self.accept_contract(address, contract_name, conditions, contract_type, testing) # accepts the contract
        return contract


    # checks the conditions of the contract
    def conditions(self):
        # function that checks whether the conditions of the contract are valid or enables the user to specify them directly
        allowed_contract_types = ["1) funding", "2) transaction", "3) other"]
        for i in range(3):
            choice = int(input(f"What type of contract do you want (1,2,3)? {allowed_contract_types}")) # asks user to specify the contract type they would like to create
            
            if choice == 1: # funding
                # When wallet A reaches X, then send Y to B
                contract_type = "funding"
                for i in range(3):
                    wallet_address = input("Which wallet must reach a certain funding goal?") # asks user for the wallet address that must reach a certain funding goal
                    if wallet_address in self.wallets: # checks if the wallet address exists
                        break
                    else: # returns an error if the wallet address provided does not exist
                        print("Wallet not found.")
                else: # this else block executes when the for loop completes normally (i.e., it didn't encounter a break)
                    raise ValueError("Failed to provide a valid wallet address after 3 attempts.")

                for i in range(3):
                    amount_total = float(input("What is the funding goal?")) # asks user for the funding goal
                    if isinstance(amount_total, float): # checks if the funding goal is a number
                        break
                    else: # returns an error if the funding goal provided is not a number
                        print("Please enter a number.")
                else: # this else block executes when the for loop completes normally (i.e., it didn't encounter a break)
                    raise ValueError("Failed to provide a valid funding goal after 3 attempts.")

                for i in range(3):
                    amount_indiv = float(input("How much will you transfer if the goal is reached?")) # asks user for the amount to transfer if the goal is reached
                    if isinstance(amount_indiv, float) and amount_indiv > 0: # checks if the amount to transfer is a number and positive
                        # contracts do not allow to transfer 0 or negative amounts, as this would not make sense in the context of the contract and without the authorization of the parties
                        break
                    else: # returns an error if the amount to transfer is not a number or not positive
                        print("Please enter a number.")
                else: # this else block executes when the for loop completes normally (i.e., it didn't encounter a break)
                    raise ValueError("Failed to provide a valid amount to transfer after 3 attempts.")

                for i in range(3):
                    receiver = input("Who will you send the money to?") # asks user for the receiver of the funds if the goal is reached
                    if receiver in self.wallets: # ensures that the receiver wallet exists
                        break
                    else: # returns an error if the receiver wallet does not exist
                        print("Wallet not found.")
                else: # this else block executes when the for loop completes normally (i.e., it didn't encounter a break)
                    raise ValueError("Failed to provide a valid receiver wallet address after 3 attempts.")

                conditions = ["When wallet ", wallet_address, " reaches ", amount_total, ", then send ", amount_indiv, " to ", receiver] # automates the inputs into the expected format
                return conditions, contract_type

            elif choice == 2: # transaction
                # When A sends money to B, I send money to C
                contract_type = "transaction"
                for i in range(3):
                    wallet_address_A = input("Which wallet must transfer an amount of tokens?") # asks user for the wallet address that must transfer an amount of tokens
                    if wallet_address_A in self.wallets:
                        break
                    else: # returns an error if the wallet address provided does not exist
                        print("Wallet not found.")
                else: # this else block executes when the for loop completes normally (i.e., it didn't encounter a break)
                    raise ValueError("Failed to provide a valid wallet address for transfer after 3 attempts.")

                for i in range(3):
                    wallet_address_B = input("To which wallet must transfer go?") # asks user for the wallet address that must receive the tokens
                    if wallet_address_B in self.wallets: # checks if the wallet address exists
                        break
                    else: # returns an error if the wallet address provided does not exist
                        print("Wallet not found.")
                else: # this else block executes when the for loop completes normally (i.e., it didn't encounter a break)
                    raise ValueError("Failed to provide a valid wallet address for receiving transfer after 3 attempts.")

                for i in range(3):
                    amount_total = float(input("How much must be transferred minimum (0 if any transaction, positive sum if transfer must have certain size and negative number if wallet receives funds)?")) # asks user for the minimum amount that must be transferred
                    if isinstance(amount_total, float): # checks if the amount to transfer is a number
                        break
                    else: # returns an error if the amount to transfer is not a number
                        print("Please enter a number.")
                else: # this else block executes when the for loop completes normally (i.e., it didn't encounter a break)
                    raise ValueError("Failed to provide a valid amount to transfer after 3 attempts.")

                for i in range(3):
                    amount_indiv = float(input(f"How much will you transfer if the the transaction between {wallet_address_A} and {wallet_address_B} occurs?")) # asks user for the amount to transfer if the transaction occurs
                    if isinstance(amount_indiv, float) and amount_indiv > 0: # checks if the amount to transfer is a number and positive
                        # contracts do not allow to transfer 0 or negative amounts, as this would not make sense in the context of the contract and without the authorization of the parties
                        break
                    else: # returns an error if the amount to transfer is not a number or not positive
                        print("Please enter a number.")
                else: # this else block executes when the for loop completes normally (i.e., it didn't encounter a break)
                    raise ValueError("Failed to provide a valid amount to transfer after 3 attempts.")

                for i in range(3):
                    receiver = input("Who will you send the money too?") # asks user for the receiver of the funds if the transaction occurs
                    if receiver in self.wallets: # ensures that the receiver wallet exists
                        break
                    else: # returns an error if the receiver wallet does not exist
                        print("Wallet not found.")
                else: # this else block executes when the for loop completes normally (i.e., it didn't encounter a break)
                    raise ValueError("Failed to provide a valid receiver wallet address after 3 attempts.")

                conditions = ["When wallet ", wallet_address_A, " transfers ", amount_total, " to ", wallet_address_B, ", then I send ", amount_indiv, " to ", receiver] # automates the inputs into the expected format
                return conditions, contract_type
            
            elif choice == 3: # other
                conditions = input("Please specify the conditions of the contract: ") # asks user to specify the conditions of the contract
                contract_type = "other" # sets contract type to 'other' as conditions could not be automated
                if not isinstance(conditions, list): # checks if conditions are in list format
                    conditions = [conditions]
                return conditions, contract_type
                
        else: # returns an error if the user does not select a valid contract type
            raise ValueError("Error. Your contract meets neither of the acceptable conditions. Please try again later.")
    

    # accepts contract
    def accept_contract(self, address, contract_name, conditions=None, contract_type=None, testing=False):
        # contract that must be accepted by each party signing a given smart contract, unless in testing mode
        contract = False
        if testing: # if in testing mode, automatically accepts the contract
            answer = "yes"

        else: # if not in testing mode, prompts user to accept the contract
            for i in range(3):
                answer = input("Did you read the conditions and accept the contract? (yes/no): ") # asks user if they wish to accept the contract based on the conditions
                if answer.lower() == "yes": # if user claims to have read the conditions and wants to accept the contract, continues
                    break
                elif answer.lower() == "no": # if user declines the contract, returns an error and does not accept the contract
                    raise ValueError("Contract not accepted.")
                else: # if user does not provide a valid input, returns an error
                    print("Invalid input. answer must be 'yes' or 'no'.")

        if answer.lower() == "yes": # if user wants to accepts the contract, continues
            if contract_name not in self.SC.keys(): # if the contract does not exist already, creates the contract
                contract = smart_contract(address, contract_name, conditions, contract_type)
                print("Contract created and accepted.")
                # stores the contract, conditions, and contract type
                self.SC[contract_name] = contract
                self.SCconditions[contract_name] = conditions
                self.SCtypes[contract_name] = contract_type
            elif contract_name in self.SC.keys(): # if the contract already exists, accepts the contract
                contract = self.SC[contract_name]
                print("Contract accepted.")

            if contract_name in self.contract_parties.keys(): # if the contract already has parties, appends the new party to the list of parties
                self.contract_parties[contract_name].append(address)
                print(f"You have signed contract {contract_name}.")
            else: # if the contract does not have parties yet, due to just having been created, creates a list of parties with the first party
                self.contract_parties[contract_name] = [address]
                print(f"You have signed contract {contract_name}.")
            
            transaction = [contract_name, address, datetime.datetime.now()] # creates a transaction for the contract to be added to the blockchain
            block_data = f"Block {len(self.chain)}" # sets the block data to the block number
            self.add_block(transaction, block_data) # adds the block to the blockchain

        return contract


    # function to show a contract or all contracts if no contract name is specified
    def show_contracts(self, contract_name=None):
        if contract_name in self.SC.keys(): # shows a specific contract, if the contract exists and is specified
            contract = self.SC[contract_name]
            parties = self.contract_parties[contract_name]
            conditions = self.SCconditions[contract_name]
            contract_type = self.SCtypes[contract_name]
            return print(f"Contract {contract_name}: \n",
                        f"{contract}\n",
                        f"Type: {contract_type}\n",
                        f"Conditions: {conditions}\n",
                        f"Parties: {parties}\n")

        elif contract_name not in self.SC.keys() and contract_name != None: # returns an error if the contract is specified but does not exist
            raise ValueError("Error. Contract not found.")

        else: # shows all contracts if no contract is specified
            for contract in self.SC.keys():
                print(f"Contract {contract} with following parties: {self.contract_parties[contract]}.")
                print(contract)
    

    # adds a party to contract
    def add_party_SC(self, address, contract_name, testing=False):
        if testing or self.authenticate_user(address): # checks to authenticate user unless in testing mode
            if contract_name in self.SC.keys(): # checks if the contract exists
                self.accept_contract(address, contract_name, testing=testing) # proceeds to accept the contract
            else: # returns an error if the contract does not exist
                raise ValueError("Error. Contract not found.")
        else: # returns an error if the user is not authenticated nor in testing mode
            raise ValueError("Error. Please try again later.")


    # function to show all parties of a contract
    def show_parties_SC(self, contract_name):        
        if contract_name in self.contract_parties.keys(): # checks if the contract exists
            parties = self.contract_parties[contract_name] # shows the parties of the contract
            return parties
        else: # returns an error if the contract does not exist
            raise ValueError("Error. Contract not found.")


    # function that automatically executes smart contracts if conditions are met, testing each contract on the blockchain
    def execute_contract(self):        
        allowed_contract_types = ["funding", "transaction", "other"]
        for contract_name, contract_type in self.SCtypes.items(): # loops through all contracts on the blockchain
            
            if contract_type in allowed_contract_types[:2]: # checks if the contract type is funding or transaction
                contract = self.SC[contract_name]
                conditions = self.SCconditions[contract_name]
                wallet_address = wallet_address_A = contract.conditions[1]
                amount_total = contract.conditions[3]

                if contract_type == allowed_contract_types[0]: # checks if the contract type is funding
                    amount_indiv = contract.conditions[5] # checks the amount to transfer if the goal is reached
                    receiver = contract.conditions[7] # checks the receiver of the funds if the goal is reached
                    if self.wallets[wallet_address].balance >= amount_total: # checks if the wallet has enough balance to reach the funding goal
                        for sender in self.contract_parties[contract_name]: # loops through all parties of the contract and executes the transaction
                            try: # executes the transaction
                                self.wallets[sender].deduct_amount(amount_indiv)
                                self.wallets[receiver].add_amount(amount_indiv)
                                print(f"Smart Contract {contract_name} executed successfully.")
                            except Exception as e: # returns an error if the contract could not be executed
                                print(f"Error. Smart Contract {contract_name} could not be executed for {sender}.")
                        self.delete_contract(contract_name, address=None) # deletes the contract after it has been executed for all parties
    
                elif contract_type == allowed_contract_types[1]: # checks if the contract type is transaction
                    wallet_address_B = contract.conditions[5] # checks the wallet that must receive the tokens
                    amount_indiv = contract.conditions[7] # checks the amount to transfer if the transaction occurs
                    receiver = contract.conditions[9] # checks the receiver of the funds if the transaction occurs
                    last_transaction = self.chain[-1].transaction # checks the last transaction on the blockchain
                    if last_transaction[0] == wallet_address_A and last_transaction[1] == wallet_address_B and last_transaction[2] == amount_total: # checks if the last transaction on the blockchain meets the conditions of the contract
                        for sender in self.contract_parties[contract_name]: # loops through all parties of the contract and executes the transaction
                            if self.wallets[sender].balance < amount_indiv: # checks if the sender has enough balance to execute the transaction
                                print("Insufficient balance. This is a breach of contract.")
                            else: # executes the transaction
                                self.wallets[sender].deduct_amount(amount_indiv)
                                self.wallets[receiver].add_amount(amount_indiv)
                                print(f"Smart Contract {contract_name} executed successfully.")


    # function that deletes a contract if all parties agree or if the creator deletes it before any parties agreed to it
    def delete_contract(self, contract_name, address):
        if address != None: # if the address is specified, checks if the user is authenticated
            if self.authenticate_user(address): # authenticates the user
                if contract_name in self.SC.keys() and len(self.contract_parties[contract_name]) == 1: # deletes the contract if the contract exists and only one party is involved
                    del self.SC[contract_name]
                    return print(f"Contract {contract_name} deleted.")
                elif contract_name in self.SC.keys() and len(self.contract_parties[contract_name]) > 1: # returns an error if the contract exists and more than one party is involved
                    raise ValueError("Contract can only be deleted if all parties agree.") # party alone cannot delete the contract without consent of all parties
                else: # returns an error if the contract does not exist
                    raise ValueError("Error. Contract not found.")
            else: # returns an error if the user is not authenticated
                raise ValueError("Error. Please try again later.")

        if address == None and contract_name in self.SC.keys(): # deletes the contract if the creator deletes it before any parties agreed to it
            del self.SC[contract_name]
            return print(f"Contract {contract_name} deleted.")


    # function that checks what the conditions of a contract are
    def check_conditions(self, contract_name):
        if contract_name in self.SC.keys(): # checks if the contract exists
            contract = self.SC[contract_name]
            contract_type = self.SCtypes[contract_name]
            conditions = self.SCconditions[contract_name]
            return print(f"Contract {contract_name} of type {contract_type} has the following conditions: {conditions}.")
        else: # returns an error if the contract does not exist
            raise ValueError("Error. Contract not found.")



############################################################################################
##################################### Other Functions ######################################
############################################################################################
# Function to fetch currency or cryptocurrency data from appropriate APIs
def fetch_currency_data(currency, is_crypto=False):
    # Base URL for cryptocurrency data; empty for traditional currencies
    base_url = "https://api.coingecko.com/api/v3" if is_crypto else ""
    # Setting the date range for the past year
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365)

    # If fetching cryptocurrency data
    if is_crypto:
        url = f"{base_url}/coins/{currency}/market_chart/range"
        params = {
            'vs_currency': 'chf',
            'from': str(int(start_date.timestamp())),
            'to': str(int(end_date.timestamp()))
        }
        response = requests.get(url, params=params)
        return response.json()  # Returning the JSON response containing the data
    else:
        # Format the currency pair for use with Yahoo Finance
        currency_pair = f"{currency}CHF=X"
        # Fetching historical data for the currency pair using Yahoo Finance
        data = yf.download(currency_pair, start=start_date, end=end_date)
        return data  # Returning the dataframe containing the currency data


# Function to parse the fetched data into usable format
def parse_data(data, is_crypto=False):
    # If the data is for cryptocurrency
    if is_crypto:
        prices = data['prices']  # Extracting price data
        dates = [datetime.datetime.fromtimestamp(price[0] / 1000.0).date() for price in prices]  # Converting timestamps to date
        values = [1 / price[1] if price[1] else None for price in prices]  # Inverting the exchange rate
    else:
        # For traditional currency, directly use the indexed data
        dates = data.index.date
        values = [1 / value if value else None for value in data['Close']]  # Inverting the exchange rate

    return dates, values  # Return parsed dates and values


# Function to plot the fetched and parsed data
def plot_data(dates, values, currency):
    plt.figure(figsize=(10, 5))
    plt.plot(dates, values, label=f'Token Price in {currency}')
    plt.xlabel('Date')
    plt.ylabel(f'{currency}')
    plt.title(f'Token Price in {currency}')
    plt.grid(True)
    plt.show()  # Displaying the plot


# Main function to handle user input and control flow
def display_crypto_price():
    currency_type = input("Do you want to see crypto or normal currency? (crypto/normal): ").strip().lower()
    if currency_type == "crypto":
        currency = input("Enter the cryptocurrency (e.g., bitcoin, ethereum): ").strip().lower()
        is_crypto = True
    else:
        while True:
            currency = input("Enter the normal currency (e.g., USD, EUR): ").strip().upper()
            if currency == "CHF":
                print("CHF is the baseline currency. Please choose another currency.")
            else:
                break
        is_crypto = False

    data = fetch_currency_data(currency, is_crypto)  # Fetching the data
    dates, values = parse_data(data, is_crypto)  # Parsing the data
    plot_data(dates, values, currency)  # Plotting the data



############################################################################################
################################### User Interface Class ###################################
############################################################################################
# User Interface Class to facilite interact with the Blockchain
class UserInterface:
    def __init__(self):
        self.blockchain = Blockchain()
        self.smart_contract = smart_contract()
        self.initiate_testing() # initiate testing mode upon initialization

    # Function to interact with the blockchain
    def menu(self):
        for i in range(3):
            print("-"*50)
            print("Welcome to the Blockchain Wallet System!")
            print("1. Create a new Wallet")             # create a new wallet
            print("2. Wallet Management")               # change password, recover wallet or delete wallet
            print("3. Transfer Funds")                  # transfer funds
            print("4. Check Wallet Balance")            # check wallet balance
            print("5. View Wallet Transaction History") # view wallet transaction history
            print("6. View Wallets Overview")           # view all wallets
            print("7. View all Transactions")           # view all transactions
            print("8. Display MACoin Price")            # display cryptocurrency price
            print("9. Display Blockchain")              # display blockchain
            print("10. Smart Contracts")                # smart contracts
            print("0. Exit")                            # exit the system
            print("-"*50)
            choice = input("Enter your choice: ")

            if choice == "1": # create a new wallet
                return self.blockchain.create_wallet()

            elif choice == "2": # change password, recover wallet or delete wallet
                for i in range(3):
                    print("-"*50)
                    print("Wallet Management")
                    print("1. Change Wallet Password")                  # change wallet password
                    print("2. Recover Wallet using Recovery Phrase")    # recover wallet using recovery phrase
                    print("3. Delete Wallet")                           # delete wallet
                    print("0. Exit")                                    # exit
                    print("-"*50)
                    choice = input("Enter your choice: ")
                    if choice in ["1", "2", "3"]:
                        address = self.get_wallet_address()
                        if choice == "1": # change wallet password
                            self.blockchain.change_password(address)
                        elif choice == "2": # recover wallet using recovery phrase
                            return self.blockchain.recover_wallet(address)
                        elif choice == "3": # delete wallet
                            return self.blockchain.delete_wallet(address)
                    elif choice == "0": # Exit
                        return print("Thank you for using the Wallet Management!\n", "-"*50)
                    else: # error message for invalid choice
                        return print("Invalid choice. Please try again.")
                raise ValueError("Error. Please try again later.") # returns an error if the user does not select a valid choice

            elif choice == "3": # transfer funds
                sender = self.get_wallet_address()
                receiver = self.get_wallet_address(transfer=True) # transfer = True when asking for wallet address of someone else (receiver)
                amount = float(input("Enter amount to transfer: "))
                #data = input("Enter transaction data: ")
                data = f"Block {len(self.blockchain.chain)}"
                return self.blockchain.transfer_funds(sender, receiver, amount, data)

            elif choice == "4": # check wallet balance
                address = self.get_wallet_address()
                balance = self.blockchain.get_wallet_balance(address)
                return print(f"Your balance is: {balance}")
            
            elif choice == "5": # view wallet transaction history
                address = self.get_wallet_address()
                return self.blockchain.print_wallet_transactions(address)
            
            elif choice == "6": # view all wallets
                return self.blockchain.print_wallets_overview()
            
            elif choice == "7": # view all transactions
                return self.blockchain.print_all_transactions()
            
            elif choice == "8": # display cryptocurrency price
                return display_crypto_price()
            
            elif choice == "9": # display blockchain
                return self.blockchain.display_chain_diagram()
            
            elif choice == "10": # smart contracts
                return self.smart_contract_menu()
            
            elif choice == "0": # Exit
                return print("Thank you for using the Blockchain Wallet System!\n", "-"*50)
            
            else: # error message for invalid choice
                return print("Invalid choice. Please try again.")
        
        raise ValueError("Error. Please try again later.") # returns an error if the user does not select a valid choice
    
    
    # Function to interact with smart contracts on the blockchain
    def smart_contract_menu(self, address=None):
        for i in range(3):
            print("-"*50)
            print("Welcome to the Smart Contracts!")
            print("1. Create a new Smart Contract")
            print("2. Sign a Smart Contract")
            print("3. Remove a Smart Contract")
            print("4. View a Smart Contract")
            print("5. View all Smart Contracts")
            print("6. Check Smart Contract conditions")
            print("7. View Smart Contract parties")
            print("8. Test the conditions of a Smart Contract")
            print("9. Show Smart Contract explanation of conditions")
            print("0. Exit")
            print("-"*50)
            choice = input("Enter your choice: ")

            if choice == "1": # create a new smart contract
                address = self.get_wallet_address() # asks user for their wallet address
                if self.blockchain.authenticate_user(address): # checks to authenticate user
                    further_choice = input("Do you already have contract conditions? (yes/no): ")
                    if further_choice.lower() == "yes": # if user already has contract conditions, proceeds to create the contract
                        conditions = input("Enter the conditions of the contract: ")
                        contract_type = input("Enter the type of the contract: ")
                        return self.blockchain.create_SC(address, conditions, contract_type)
                    else: # if user does not have contract conditions, proceeds to create the contract
                        return self.blockchain.create_SC(address)
                else: # returns an error if the user is not authenticated
                    raise ValueError("Error. Could not create contract. Please try again later.")

            elif choice == "2": # sign a smart contract
                contract_name = self.get_contract_name() # asks user for the name of the contract
                address = self.get_wallet_address() # asks user for their wallet address
                return self.blockchain.add_party_SC(address, contract_name)
            
            elif choice == "3": # remove a smart contract
                contract_name = self.get_contract_name() # asks user for the name of the contract
                address = self.get_wallet_address() # asks user for their wallet address
                return self.blockchain.delete_contract(address, contract_name)
            
            elif choice == "4": # view a smart contract
                contract_name = self.get_contract_name() # asks user for the name of the contract
                return self.blockchain.show_contracts(contract_name)

            elif choice == "5": # view all smart contracts
                return self.blockchain.show_contracts()
            
            elif choice == "6": # check smart contract conditions
                contract_name = self.get_contract_name() # asks user for the name of the contract
                return self.blockchain.check_conditions(contract_name)

            elif choice == "7": # view smart contract parties
                contract_name = self.get_contract_name() # asks user for the name of the contract
                return self.blockchain.show_parties_SC(contract_name)

            elif choice == "8": # test the conditions of a smart contract
                contract_name = self.get_contract_name() # asks user for the name of the contract
                return self.blockchain.execute_contract(contract_name)
            
            elif choice == "9": # show smart contract explanation of conditions
                return self.smart_contract.explain_conditions() # shows the explanation of standardized contract types
            
            elif choice == "0": # Exit
                return print("Thank you for using the Blockchain System!\n", "-"*50)
            
            else: # error message for invalid choice
                print("Invalid choice. Please try again.")

        raise ValueError("Error. Please try again later.") # returns an error if the user does not select a valid choice
    
    
    # Function to get the name of the contract from the user
    def get_contract_name(self):
        for i in range(3):
            contract_name = input("Enter the name of the contract: ") # asks user for the name of the contract
            if contract_name in self.blockchain.SC.keys(): # checks if the contract exists
                return contract_name
            else: # returns an error if the contract does not exist
                print("Contract not found.")
        raise ValueError("Error. Please try again later.") # returns an error if the user does not select a valid choice


    # Function to get the wallet address from the user
    def get_wallet_address(self, transfer=None):
        if transfer: # transfer = True when asking for wallet address of someone else (receiver)
            for i in range(3):
                address = input("Enter the receiver's wallet address: ") # asks user for the receiver's wallet address
                if address in self.blockchain.wallets: # checks if the wallet address exists
                    return address
                else: # returns an error if the wallet address provided does not exist
                    print("Wallet not found.")
            raise ValueError("Error. Please try again later.") # returns an error if the user does not select a valid choice

        else: # transfer = None for when asking user for own wallet address
            for i in range(3):
                address = input("Enter your wallet address: ") # asks user for their wallet address
                if address in self.blockchain.wallets: # checks if the wallet address exists
                    return address
                else: # returns an error if the wallet address provided does not exist
                    print("Wallet not found.")
            raise ValueError("Error. Please try again later.") # returns an error if the user does not select a valid choice
        

    # function invoked in __init__ method after instantiation
    def initiate_testing(self):
        # initiates testing mode, asking user if they want to create numerous contracts, transactions or smart contracts
        choice = input("Do you want to initiate the Blockchain by creating numerous contracts, transactions or smart contracts? (yes/no): ")
        if choice.lower() == "yes": # initiates testing mode if desired
            return self.testing_UI()
        else: # exits if user does not want to initiate testing mode
            return print("-"*50, "\nThank you for using the Blockchain Wallet System!\n", "-"*50)
        

    # User Interface for initiating the Blockchain and adding numerous wallets etc
    def testing_UI(self):
        print("-"*50)
        print("Welcome to the Blockchain testing interface!")
        print("1. Create Wallets")
        print("2. Create Smart Contracts")
        print("3. Create Transactions")
        print("0. Exit")
        print("-"*50)
        choice = input("Enter your choice: ")
        
        for i in range(3):
            if choice == "1": # creates wallets
                return self.create_test_wallets()
            elif choice == "2": # creates smart contracts
                return self.create_test_contracts()
            elif choice == "3": # creates transactions
                return self.create_test_transactions()
            elif choice == "0": # Exits
                return print("Thank you for using the Blockchain Wallet System!\n", "-"*50)
            else: # error message for invalid choice
                return print("Invalid choice. Please try again.")
        raise ValueError("Error. Please try again later.") # returns an error if the user does not select a valid choice
    
    
    # function to create numerous test wallets on the blockchain
    def create_test_wallets(self, number=10):
        for i in range(number):
            self.blockchain.create_wallet(testing=True)


    # function to create numerous test transactions on the blockchain with the wallets created
    def create_test_transactions(self, number=10):
        for i in range(number):
            num = secrets.randbelow(len(self.blockchain.wallets))
            num1 = secrets.randbelow(len(self.blockchain.wallets))
            if num != num1: # ensures that the sender and receiver are not the same
                sender = list(self.blockchain.wallets.keys())[num] # selects a random sender
                receiver = list(self.blockchain.wallets.keys())[num1] # selects a random receiver
                amount = secrets.randbelow(10)+1 # selects a random amount between 1 and 10
                if amount <= self.blockchain.wallets[sender].balance: # ensures that the sender has enough balance to transfer the amount
                    data = f"Transaction {i+1}"
                    self.blockchain.transfer_funds(sender, receiver, amount, data, testing=True) # transfers the funds

    
    # function to create numerous test smart contracts on the blockchain
    def create_test_contracts(self, number=5):
        for i in range(number): # creates a number of smart contracts of type "funding" with a funding goal of 150 and own transfer of 5
            address = secrets.choice(list(self.blockchain.wallets.keys()))
            conditions = ["When wallet ", secrets.choice(list(self.blockchain.wallets.keys())), " reaches ", 150, ", then send ", 5, " to ", secrets.choice(list(self.blockchain.wallets.keys()))]
            contract_type = "funding"
            self.blockchain.create_SC(address, conditions, contract_type, testing=True) # creates the contract

        for i in range(number): # creates a number of smart contracts of type "transaction" with a transfer of 20 and own transfer of 5
            address = secrets.choice(list(self.blockchain.wallets.keys()))
            conditions = ["When wallet ", secrets.choice(list(self.blockchain.wallets.keys())), " transfers ", 20, " to ", secrets.choice(list(self.blockchain.wallets.keys())), ", then I send ", 5, " to ", secrets.choice(list(self.blockchain.wallets.keys()))]
            contract_type = "transaction"
            self.blockchain.create_SC(address, conditions, contract_type, testing=True) # creates the contract

        for i in range(number): # adds random parties to random existing smart contracts
            contract_name = secrets.choice(list(self.blockchain.SC.keys())) # selects a random smart contract
            address = secrets.choice(list(self.blockchain.wallets.keys())) # selects a random wallet
            self.blockchain.add_party_SC(address, contract_name, testing=True) # adds the party to the smart contract

# %% [markdown]
# ## Blockchain interaction

# %%
# to initiate the User Interface
UI = UserInterface()

# %%
# to display the testing User Interface
UI.testing_UI()

# %%
# to display the main User Interface
UI.menu()

# %% [markdown]
# ### Alternative approach: interacting with blockchain without UI

# %%
# initiate the Blockchain
chain = Blockchain()

# %%
# Examplary commands to create wallets, directly on the blockchain chain
w1 = chain.create_wallet()
w2 = chain.create_wallet()
chain.transfer_funds(w1, w2, 10, "First Transaction")
chain.transfer_funds(w1, w2, 50, "Another Transaction")
chain.get_wallet_balance(w1)
chain.get_wallet_balance(w2)
chain.print_wallet_transactions(w1)
chain.print_chain()
