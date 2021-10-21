# Initializing our blockchain list
genesis_block = {
    'previous_hash' : '',
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

def add_transaction(recipient, sender = owner, amount = 1.0):
    '''Append a new value of transactions
        Arguments:
            - sender : The sender of the coins
            - recipient : The recipient of the coins
            - amount : The amount of coins sent with the transaction (default = 1.0)
    '''
    transaction = {
        'sender' : sender,
        'recipient' : recipient,
        'amount' : amount
    }
    open_transactions.append(transaction)
    participants.add(sender)
    participants.add(recipient)

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



def menu():
    print("1 : Add transaction")
    print("2 : Print the current blockchain")
    print("3 : Print  participants")
    print("q : Quit")

while True:
    menu()
    choice = input("Enter your choice : ")
    if choice == '1':
        data = get_transaction_value()
        recipient, amount = data 
        add_transaction(
            recipient = recipient, 
            amount = amount
        )
        print(open_transactions)
    elif choice == '2':
        print_blockchain()
    elif choice == '3':
        print(participants)
    elif choice == 'q':
        break 
    else:
        print("Invalid choice!")

print("User left!")