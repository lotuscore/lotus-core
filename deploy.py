"""Deploy Lotus token and smart contract.

A simple Python script to deploy contracts and then do a smoke test for them.
"""
import os

from populus import Project
from populus.utils.cli import get_unlocked_default_account_address
from populus.utils.wait import wait_for_transaction_receipt
from web3 import Web3


def check_succesful_tx(web3: Web3, txid: str, timeout=180) -> dict:
    """See if transaction went through (Solidity code did not throw).

    :return: Transaction receipt
    """

    # http://ethereum.stackexchange.com/q/6007/620
    receipt = wait_for_transaction_receipt(web3, txid, timeout=timeout)
    txinfo = web3.eth.getTransaction(txid)

    # EVM has only one error mode and it's consume all gas
    assert txinfo["gas"] != receipt["gasUsed"]
    return receipt


def main():

    project = Project()

    chain_name = os.environ.get('CHAIN', 'external')
    print("Make sure {} chain is running, you can connect to it, "
          "or you'll get timeout".format(chain_name))

    with project.get_chain(chain_name) as chain:

        # Load Populus contract proxy classes
        Token = chain.provider.get_contract_factory('LotusToken')

        web3 = chain.web3
        print("Web3 provider is", web3.currentProvider)

        # The address who will be the owner of the contracts
        beneficiary = web3.eth.coinbase
        assert beneficiary, "Make sure your node has coinbase account created"

        # Goes through coinbase account unlock process if needed
        if chain_name in ['mainnet', 'ropsten']:
            get_unlocked_default_account_address(chain)

        # Deploy token
        txhash = Token.deploy(transaction={
            "from": beneficiary
        })
        print("Deploying token, tx hash is", txhash)
        receipt = check_succesful_tx(web3, txhash)
        token_address = receipt["contractAddress"]
        print("Token contract address is", token_address)

        token = Token(address=token_address)

        # Do some contract reads to see everything looks ok
        print("Token total supply is", token.call().totalSupply())

        print("All done! Enjoy your decentralized future.")


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core'))
    main()