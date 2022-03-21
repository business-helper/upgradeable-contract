from brownie import (
    accounts,
    network,
    config,
)
import eth_utils

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "hardhat",
    "development",
    "ganache-local",
    "ganache-gui",
    "mainnet-fork",
]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add(key)
    # accounts.load(id)
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


# initializer=box.store, 1,2,3,4
def encode_function_data(initializer=None, *args):
    """Encodes the function call so we can work with an initializer.
    Args:
        initializer ([brownie.network.contract.ContractTx], optional):
        The initializer function we want to call. Example: `box.store`.
        Defaults to None.
        args (Any, optional):
        The arguments to pass to the initializer function
    Returns:
        [bytes]: Return the encoded bytes.
    """
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


def upgrade(
    account,
    proxy,
    new_implementation_address,
    proxy_admin_contract=None,
    initializer=None,
    *args
):
    if proxy_admin_contract:
      if initializer:
        encoded_function_call = encode_function_data(initializer, *args)
        transaction = proxy_admin_contract.upgradeAndCall(
          proxy.address,
          new_implementation_address,
          encoded_function_call,
          {"from": account}
        )
      else:
        transaction = proxy_admin_contract.upgrade(
          proxy.address,
          new_implementation_address,
          {"from": account}
        )
    else:
      if (initializer):
        encoded_function_call = encode_function_data(initializer, *args)
        transaction = proxy.upgradaeAndCall(
          new_implementation_address, encoded_function_call, {"from": account}
        )
      else:
        transaction = proxy.upgrade(
          new_implementation_address, {"from": account}
        )
    return transaction
