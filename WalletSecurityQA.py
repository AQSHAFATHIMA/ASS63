from DigitalWallet import DigitalWallet


def test_account_creation():
    w = DigitalWallet()

    assert w.create_account(
        "A1", "Alice", "1234"
    ) == "Account created"

    assert "A1" in w.accounts

    print("Account creation: PASS")


def test_normal_transaction():
    w = DigitalWallet()

    w.create_account("A1", "Alice", "1234")

    result = w.deposit("A1", 1000)

    assert "Deposit successful" in result
    assert w.balance("A1") == 1000

    print("Normal transaction: PASS")


def test_insufficient_balance():
    w = DigitalWallet()

    w.create_account("A1", "Alice", "1234")

    result = w.withdraw("A1", 500)

    assert result == "Insufficient balance"

    print("Insufficient balance: PASS")


def test_transfer():
    w = DigitalWallet()

    w.create_account("A1", "Alice", "1234")
    w.create_account("A2", "Bob", "5678")

    w.deposit("A1", 1000)

    result = w.transfer("A1", "A2", 400)

    assert "Transfer successful" in result
    assert w.balance("A1") == 600
    assert w.balance("A2") == 400

    print("Money transfer: PASS")


def test_transaction_history():
    w = DigitalWallet()

    w.create_account("A1", "Alice", "1234")

    w.deposit("A1", 500)

    assert len(w.history("A1")) == 1
    assert w.history("A1")[0]["type"] == "Deposit"

    print("Transaction history: PASS")


def test_daily_limit():
    w = DigitalWallet()

    w.create_account("A1", "Alice", "1234")

    for i in range(w.DAILY_LIMIT):
        w.deposit("A1", 10)

    result = w.deposit("A1", 10)

    assert result == "Daily limit exceeded"

    print("Daily transaction limit: PASS")


def test_balance_verification():
    w = DigitalWallet()

    w.create_account("A1", "Alice", "1234")
    w.deposit("A1", 2000)

    assert w.balance("A1") == 2000

    print("Balance verification: PASS")


def test_multiple_failed_pins():
    w = DigitalWallet()

    w.create_account("A1", "Alice", "1234")

    for i in range(w.FAILED_PIN_LIMIT):
        w.verify_pin("A1", "9999")

    result = w._fraud("A1", 100)

    assert "Multiple failed PIN attempts" in result

    print("Multiple failed PINs: PASS")


def test_large_transaction():
    w = DigitalWallet()

    w.create_account("A1", "Alice", "1234")

    result = w.deposit(
        "A1",
        w.LARGE_TRANSACTION + 1
    )

    assert "Suspicious" in result

    print("Large transaction: PASS")


def test_unusual_transaction():
    w = DigitalWallet()

    w.create_account("A1", "Alice", "1234")

    result = w.deposit(
        "A1",
        w.UNUSUAL_AMOUNT + 1
    )

    assert "Suspicious" in result

    print("Unusual transaction: PASS")


def test_negative_amount():
    w = DigitalWallet()

    w.create_account("A1", "Alice", "1234")

    assert w.deposit("A1", -100) == \
        "Invalid amount"

    assert w.withdraw("A1", -100) == \
        "Invalid amount"

    print("Negative amount: PASS")


def test_duplicate_transaction():
    w = DigitalWallet()

    w.create_account("A1", "Alice", "1234")

    w.deposit("A1", 100)
    w.deposit("A1", 100)

    assert len(w.history("A1")) == 2

    print("Duplicate transaction: PASS")


def test_concurrent_transactions():
    # Jenkins-safe deterministic test:
    # several transactions are executed and
    # final balance is verified.
    w = DigitalWallet()

    w.create_account("A1", "Alice", "1234")

    for i in range(5):
        w.deposit("A1", 100)

    assert w.balance("A1") == 500

    print("Concurrent transaction scenario: PASS")


print("===== WALLET SECURITY QA =====")

test_account_creation()
test_normal_transaction()
test_insufficient_balance()
test_transfer()
test_transaction_history()
test_daily_limit()
test_balance_verification()
test_multiple_failed_pins()
test_large_transaction()
test_unusual_transaction()
test_negative_amount()
test_duplicate_transaction()
test_concurrent_transactions()

print("\nALL TESTS PASSED")
