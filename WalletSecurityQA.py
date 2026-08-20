from DigitalWallet import DigitalWallet
from threading import Thread


def test_normal_transaction():

    w = DigitalWallet()

    assert w.create_account("A1", "User1", "1234") == \
        "Account created successfully"

    assert w.deposit("A1", 1000) == \
        "Deposit successful"

    assert w.balance("A1") == 1000

    print("Normal transaction: PASS")


def test_insufficient_balance():

    w = DigitalWallet()

    w.create_account("A1", "User1", "1234")
    w.deposit("A1", 500)

    result = w.withdraw("A1", 1000)

    assert result == "Insufficient balance"

    print("Insufficient balance: PASS")


def test_daily_limit():

    w = DigitalWallet()

    w.create_account("A1", "User1", "1234")

    for i in range(w.DAILY_TRANSACTION_LIMIT):
        w.deposit("A1", 10)

    result = w.deposit("A1", 10)

    assert result == "Daily transaction limit exceeded"

    print("Daily transaction limit: PASS")


def test_multiple_failed_pins():

    w = DigitalWallet()

    w.create_account("A1", "User1", "1234")

    for i in range(w.FAILED_PIN_LIMIT):
        w.verify_pin("A1", "9999")

    result = w.fraud_check("A1", 100)

    assert "Multiple failed PIN attempts" in result

    print("Multiple failed PINs: PASS")


def test_suspicious_transaction():

    w = DigitalWallet()

    w.create_account("A1", "User1", "1234")

    result = w.deposit(
        "A1",
        w.LARGE_TRANSACTION + 1
    )

    assert "SUSPICIOUS" in result

    print("Suspicious transaction: PASS")


def test_duplicate_transaction():

    w = DigitalWallet()

    w.create_account("A1", "User1", "1234")

    w.deposit("A1", 100)

    first_history = len(w.history("A1"))

    # Same transaction repeated
    w.deposit("A1", 100)

    second_history = len(w.history("A1"))

    assert second_history > first_history

    print("Duplicate transaction: PASS")


def test_negative_amount():

    w = DigitalWallet()

    w.create_account("A1", "User1", "1234")

    assert w.deposit("A1", -100) == \
        "Invalid amount"

    assert w.withdraw("A1", -100) == \
        "Invalid amount"

    print("Negative amount: PASS")


def transaction(w):

    w.deposit("A1", 100)


def test_concurrent_transactions():

    w = DigitalWallet()

    w.create_account("A1", "User1", "1234")

    threads = []

    for i in range(5):
        t = Thread(
            target=transaction,
            args=(w,)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert w.balance("A1") == 500

    print("Concurrent transactions: PASS")


# Run all tests

print("===== WALLET SECURITY QA =====")

test_normal_transaction()
test_insufficient_balance()
test_daily_limit()
test_multiple_failed_pins()
test_suspicious_transaction()
test_duplicate_transaction()
test_negative_amount()
test_concurrent_transactions()

print("\nALL TESTS PASSED")
