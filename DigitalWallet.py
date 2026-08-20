from datetime import datetime, timedelta

class DigitalWallet:

    # Configurable limits
    DAILY_TRANSACTION_LIMIT = 10
    LARGE_TRANSACTION = 50000
    FAILED_PIN_LIMIT = 3
    UNUSUAL_TRANSACTION = 100000

    def __init__(self):
        self.accounts = {}

    # Account Creation
    def create_account(self, account, name, pin):
        if account in self.accounts:
            return "Account already exists"

        if len(pin) != 4 or not pin.isdigit():
            return "Invalid PIN"

        self.accounts[account] = {
            "name": name,
            "pin": pin,
            "balance": 0.0,
            "history": [],
            "failed_pins": 0
        }

        return "Account created successfully"

    # PIN Verification
    def verify_pin(self, account, pin):
        if account not in self.accounts:
            return False

        if self.accounts[account]["pin"] == pin:
            self.accounts[account]["failed_pins"] = 0
            return True

        self.accounts[account]["failed_pins"] += 1
        return False

    # Fraud Detection
    def fraud_check(self, account, amount):

        data = self.accounts[account]
        now = datetime.now()

        # More than 5 transactions in 10 minutes
        recent = 0
        for t in data["history"]:
            if now - t["time"] <= timedelta(minutes=10):
                recent += 1

        if recent >= 5:
            return "SUSPICIOUS: More than 5 transactions in 10 minutes"

        # Multiple failed PIN attempts
        if data["failed_pins"] >= self.FAILED_PIN_LIMIT:
            return "SUSPICIOUS: Multiple failed PIN attempts"

        # Large transaction
        if amount > self.LARGE_TRANSACTION:
            return "SUSPICIOUS: Large transaction"

        # Unusual transaction amount
        if amount > self.UNUSUAL_TRANSACTION:
            return "SUSPICIOUS: Unusual transaction amount"

        return "SAFE"

    # Daily Transaction Limit
    def daily_limit_check(self, account):

        today = datetime.now().date()

        count = 0

        for t in self.accounts[account]["history"]:
            if t["time"].date() == today:
                count += 1

        return count < self.DAILY_TRANSACTION_LIMIT

    # Deposit
    def deposit(self, account, amount):

        if account not in self.accounts:
            return "Account not found"

        if amount <= 0:
            return "Invalid amount"

        if not self.daily_limit_check(account):
            return "Daily transaction limit exceeded"

        fraud = self.fraud_check(account, amount)

        self.accounts[account]["balance"] += amount

        self.accounts[account]["history"].append({
            "type": "Deposit",
            "amount": amount,
            "time": datetime.now(),
            "status": fraud
        })

        if fraud != "SAFE":
            return "Deposit successful - " + fraud

        return "Deposit successful"

    # Withdrawal
    def withdraw(self, account, amount):

        if account not in self.accounts:
            return "Account not found"

        if amount <= 0:
            return "Invalid amount"

        if amount > self.accounts[account]["balance"]:
            return "Insufficient balance"

        if not self.daily_limit_check(account):
            return "Daily transaction limit exceeded"

        fraud = self.fraud_check(account, amount)

        self.accounts[account]["balance"] -= amount

        self.accounts[account]["history"].append({
            "type": "Withdrawal",
            "amount": amount,
            "time": datetime.now(),
            "status": fraud
        })

        if fraud != "SAFE":
            return "Withdrawal successful - " + fraud

        return "Withdrawal successful"

    # Money Transfer
    def transfer(self, sender, receiver, amount):

        if sender not in self.accounts:
            return "Sender account not found"

        if receiver not in self.accounts:
            return "Receiver account not found"

        if sender == receiver:
            return "Invalid transfer"

        if amount <= 0:
            return "Invalid amount"

        if amount > self.accounts[sender]["balance"]:
            return "Insufficient balance"

        if not self.daily_limit_check(sender):
            return "Daily transaction limit exceeded"

        fraud = self.fraud_check(sender, amount)

        self.accounts[sender]["balance"] -= amount
        self.accounts[receiver]["balance"] += amount

        self.accounts[sender]["history"].append({
            "type": "Transfer",
            "amount": amount,
            "receiver": receiver,
            "time": datetime.now(),
            "status": fraud
        })

        self.accounts[receiver]["history"].append({
            "type": "Received",
            "amount": amount,
            "sender": sender,
            "time": datetime.now(),
            "status": fraud
        })

        if fraud != "SAFE":
            return "Transfer successful - " + fraud

        return "Transfer successful"

    # Balance Verification
    def balance(self, account):

        if account not in self.accounts:
            return "Account not found"

        return self.accounts[account]["balance"]

    # Transaction History
    def history(self, account):

        if account not in self.accounts:
            return "Account not found"

        return self.accounts[account]["history"]


# ---------------- MAIN PROGRAM ----------------

wallet = DigitalWallet()

print("===== DIGITAL WALLET =====")

account = input("Enter Account ID: ")
name = input("Enter Name: ")
pin = input("Create 4-digit PIN: ")

print(wallet.create_account(account, name, pin))

# Create another account for transfer
receiver = input("Enter Receiver Account ID: ")
receiver_name = input("Enter Receiver Name: ")
receiver_pin = input("Enter Receiver 4-digit PIN: ")

print(wallet.create_account(receiver, receiver_name, receiver_pin))

print("\n1. Deposit")
print("2. Withdraw")
print("3. Transfer")
print("4. Balance")
print("5. Transaction History")

choice = input("Enter choice: ")

entered_pin = input("Enter PIN: ")

if not wallet.verify_pin(account, entered_pin):
    print("Invalid PIN")
    print("Failed PIN attempts:",
          wallet.accounts[account]["failed_pins"])

else:

    if choice == "1":

        amount = float(input("Enter deposit amount: "))
        print(wallet.deposit(account, amount))

    elif choice == "2":

        amount = float(input("Enter withdrawal amount: "))
        print(wallet.withdraw(account, amount))

    elif choice == "3":

        amount = float(input("Enter transfer amount: "))
        print(wallet.transfer(account, receiver, amount))

    elif choice == "4":

        print("Current Balance:",
              wallet.balance(account))

    elif choice == "5":

        print("\nTransaction History:")

        for t in wallet.history(account):
            print(t)

    else:
        print("Invalid choice")

print("\nFinal Balance:",
      wallet.balance(account))
