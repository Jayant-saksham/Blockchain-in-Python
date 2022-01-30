from hash_utils import hash_string_256, hash_block
MINING_REWARD = 10
from collections import OrderedDict
import json

# Initializing our blockchain list
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100,
}

blockchain = [genesis_block]
open_transactions = []
owner = 'Jayant'
participants = {owner}


def save_data():
    with open('blockchain.txt', mode='w') as f:
        f.write(json.dumps(blockchain))
        f.write("\n")
        f.write(json.dumps(open_transactions))


def load_data():
    with open('blockchain.txt', mode = 'r') as f:
        file_content = f.readlines()
        global blockchain
        global open_transactions
        blockchain = json.loads(file_content[0][:-1])
        open_transactions = json.loads(file_content[1])


load_data()

def get_last_blockchain():
    '''Returns the last value of the current blockchain'''
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def valid_proof(transaction, last_hash, proof):
    '''It validates the current Nonce
        - Transactions
        - Previous Hash
        - Nonce: Number used only once
    '''
    guess = (str(transaction) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    if guess_hash[0:2] == '00':
        return True
    return False


def proof_of_work():
    '''Returns the correct proof'''
    last_block = get_last_blockchain()
    lash_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, lash_hash, proof):
        proof += 1
    return proof


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    if sender_balance >= transaction['amount']:
        return True
    return False


def add_transaction(recipient, sender=owner, amount=1.0):
    '''Append a new value of transactions
        Arguments:
            - sender : The sender of the coins
            - recipient : The recipient of the coins
            - amount : The amount of coins sent with the transaction (default = 1.0)
    '''
    transaction = OrderedDict(
        [('sender', sender), ('recipient', recipient), ('amount', amount)]
    )
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def get_balance(participant=owner):
    '''Returns the remaining balance'''
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        amount_sent += sum(tx)

    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]
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
    # reward_transaction = OrderedDict(
    #     [('sender': 'MINING'), ('recipient', owner), ('amount', MINING_REWARD) ]
    # )
    proof = proof_of_work()
    open_transactions.append(reward_transaction)
    if last_block is not None:
        hash_last_block = hash_block(last_block)
        block = {
            'previous_hash': hash_last_block,
            'index': len(blockchain),
            'transactions': open_transactions,
            'proof': proof,
        }
        blockchain.append(block)
        save_data()
        return True
    return False

def verify_chain():
    '''Verifies the current blockchain and return True if it is valid'''
    for index, block in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False
    return True


def menu():
    print("1 : Add transaction")
    print("2 : Print the current blockchain")
    print("3 : Print  participants")
    print("4 : Mine the block")
    print("5 : Hack the blockchain")
    print("q : Quit")


while True:
    menu()
    choice = input("Enter your choice : ")
    if choice == '1':
        data = get_transaction_value()
        recipient, amount = data
        if add_transaction(
            recipient=recipient,
            amount=amount
        ):
            print("Transaction success")
        else:
            print("Invalid transaction")
    elif choice == '2':
        print_blockchain()
    elif choice == '3':
        print(participants)
    elif choice == '4':
        if mine_block():
            open_transactions = []
    elif choice == '5':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{
                    'sender': "Prateek",
                    'recipient': "Sudershan",
                    'amount': 500,
                }]
            }
    elif choice == 'q':
        break
    else:
        print("Invalid choice!")
    print(open_transactions)
    print(get_balance())
    if not verify_chain():
        print("INvalid Blockchain")
        break

print("User left!")
