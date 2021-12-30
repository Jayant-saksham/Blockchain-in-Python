from hashlib import sha256
from json import dumps
MINING_REWARD = 10

# Initializing our blockchain list
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}

blockchain = [genesis_block]
open_transactions = []
owner = 'Jayant'
participants = {owner}


def get_last_blockchain():
    '''Returns the last value of the current blockchain'''
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def hash_block(block):
    '''Generates a hash for the given block'''
    return sha256(dumps(block).encode()).hexdigest()
    

def add_transaction(recipient, sender=owner, amount=1.0):
    '''Append a new value of transactions
        Arguments:
            - sender : The sender of the coins
            - recipient : The recipient of the coins
            - amount : The amount of coins sent with the transaction (default = 1.0)
    '''
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    open_transactions.append(transaction)
    participants.add(sender)
    participants.add(recipient)


def get_balance(participant = owner):
    '''Returns the remaining balance'''
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    amount_sent = 0
    for tx in tx_sender:
        amount_sent += sum(tx)

    
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_recivied = 0
    for tx in tx_recipient:
        amount_recivied += sum(tx) 

    return amount_recivied - amount_sent



def get_transaction_value():
    '''Returns the input of the user'''
    tx_recipient = input("Enter recipient of the transaction : ")
    tx_amount = float(input("Enter amount : "))
    data = (tx_recipient, tx_amount)
    return data


def print_blockchain():
    '''Prints the blockchain'''
    for block in blockchain:
        print(block)
    print("\n")
    print("-" * 20)


def mine_block():
    '''Mining the block to the current blockchain'''
    last_block = get_last_blockchain()
    reward_transaction = {
        'sender': "MINING",
        'recipient': owner,
        'amount': MINING_REWARD,
    }
    open_transactions.append(reward_transaction)
    if last_block is not None:
        hash_last_block = hash_block(last_block)
        block = {
            'previous_hash': hash_last_block,
            'index': len(blockchain),
            'transactions': open_transactions
        }
        blockchain.append(block)
        return True
    return False


def menu():
    print("1 : Add transaction")
    print("2 : Print the current blockchain")
    print("3 : Print  participants")
    print("4 : Mine the block")
    print("q : Quit")


while True:
    menu()
    choice = input("Enter your choice : ")
    if choice == '1':
        data = get_transaction_value()
        recipient, amount = data
        add_transaction (
            recipient = recipient,
            amount = amount
        )
    elif choice == '2':
        print_blockchain()
    elif choice == '3':
        print(participants)
    elif choice == '4':
        if mine_block():
            open_transactions = []
    elif choice == 'q':
        break
    else:
        print("Invalid choice!")
    print(open_transactions)
    print(get_balance())

print("User left!")
