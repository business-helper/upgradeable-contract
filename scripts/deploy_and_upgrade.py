from brownie import (
    network,
    config,
    Contract,
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
)
from scripts.helpful_scripts import get_account, encode_function_data, upgrade


def main():
    account = get_account()
    print(f"Depoying to {network.show_active()}...")

    box = Box.deploy({"from": account})
    print(box.retrieve())

    proxy_admin = ProxyAdmin.deploy({"from": account})

    initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data(initializer)

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gast_limit": 1000000},
    )
    print(f"Proxy deployed at {proxy}, you can upgrade to v2!")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    tx = proxy_box.store(1, {"from": account})
    tx.wait(1)
    print(f"Box value is {proxy_box.retrieve()}")

    # upgrade
    box_v2 = BoxV2.deploy({"from": account})
    upgrade_tx = upgrade(
      account,
      proxy,
      box_v2.address,
      proxy_admin_contract=proxy_admin,
    )
    upgrade_tx.wait(1)

    proxy_box = Contract.from_abi('BoxV2', proxy.address, BoxV2.abi)
    increase_tx = proxy_box.increment({"from": account})
    increase_tx.wait(1)
    print(proxy_box.retrieve())

