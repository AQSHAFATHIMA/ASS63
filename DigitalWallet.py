from datetime import datetime, timedelta


class DigitalWallet:

    DAILY_LIMIT = 10
    LARGE_TRANSACTION = 50000
    UNUSUAL_AMOUNT = 100000
    FAILED_PIN_LIMIT = 3

    def __init__(self):
        self.accounts = {}

    def create_account(self, acc, name, pin):
        if acc in self.accounts:
            return "Account already exists"

        self.accounts[acc] = {
            "name": name,
            "pin": pin,
            "balance": 0,
            "transactions": [],
            "failed_pins": 0
        }
        return "Account created"

    def verify_pin(self, acc, pin):
        if self.accounts[acc]["pin"] == pin:
            self.accounts[acc]["failed_pins"] = 0
            return True

        self.accounts[acc]["failed_pins"] += 1
        return False

    def _limit(self, acc):
        today = datetime.now().date()
        count = sum(
            1 for t in self.accounts[acc]["transactions"]
            if t["time"].date() == today
        )
        return count < self.DAILY_LIMIT

    def _fraud(self, acc, amount):
        data = self.accounts[acc]
        now = datetime.now()

        recent = sum(
            1 for t in data["transactions"]
            if now - t["time"] <= timedelta(minutes=10)
        )

        if recent >= 5:
            return "Suspicious: More than 5 transactions in 10 minutes"

        if data["failed_pins"] >= self.FAILED_PIN_LIMIT:
            return "Suspicious: Multiple failed PIN attempts"

        if amount > self.UNUSUAL_AMOUNT:
            return "Suspicious: Unusual transaction amount"

        if amount > self.LARGE_TRANSACTION:
            return "Suspicious: Large transaction"

        return "Safe"

    def _record(self, acc, typ, amount):
        status = self._fraud(acc, amount)

        self.accounts[acc]["transactions"].append({
            "type": typ,
            "amount": amount,
            "time": datetime.now(),
            "status": status
        })

        return status

    def deposit(self, acc, amount):
        if amount <= 0:
            return "Invalid amount"

        if not self._limit(acc):
            return "Daily limit exceeded"

        self.accounts[acc]["balance"] += amount
        status = self._record(acc, "Deposit", amount)

        return "Deposit successful - " + status

    def withdraw(self, acc, amount):
        if amount <= 0:
            return "Invalid amount"

        if amount > self.accounts[acc]["balance"]:
            return "Insufficient balance"

        if not self._limit(acc):
            return "Daily limit exceeded"

        self.accounts[acc]["balance"] -= amount
        status = self._record(acc, "Withdrawal", amount)

        return "Withdrawal successful - " + status

    def transfer(self, sender, receiver, amount):
        if amount <= 0:
            return "Invalid amount"

        if amount > self.accounts[sender]["balance"]:
            return "Insufficient balance"

        if not self._limit(sender):
            return "Daily limit exceeded"

        self.accounts[sender]["balance"] -= amount
        self.accounts[receiver]["balance"] += amount

        status = self._record(sender, "Transfer", amount)

        return "Transfer successful - " + status

    def balance(self, acc):
        return self.accounts[acc]["balance"]

    def history(self, acc):
        return self.accounts[acc]["transactions"]
