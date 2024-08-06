# Simple Vyper contract to store and retrieve a value

# Declare a public variable to store the value
storedData: public(uint256)

@external
def set(data: uint256):
    """
    Function to set the value of storedData.
    """
    self.storedData = data

@external
def get() -> uint256:
    """
    Function to get the value of storedData.
    """
    return self.storedData
