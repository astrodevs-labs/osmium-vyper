# SPDX-License-Identifier: MIT

# With vulnerabilities
contract_balance: public(uint256)

@external
def set_balance(new_balance: uint256):
    self.contract_balance = new_balance

@external
def add_balance(amount: uint256):
    self.contract_balance += amount

@external
def subtract_balance(amount: uint256):
    self.contract_balance -= amount

@external
def get_balance() -> uint256:
    return self.contract_balance

@external
def transfer(receiver: address, amount: uint256):
    assert self.contract_balance >= amount, "Insufficient balance"
    self.contract_balance -= amount
    raw_call(receiver, b"", value=amount)
# With vulnerabilities

