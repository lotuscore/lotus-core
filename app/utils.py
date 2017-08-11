import os

from populus import Project
from populus.utils.wait import wait_for_transaction_receipt
from web3 import Web3


def get_chain():
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),
             '..', 'core'))
    project = Project()
    chain_name = os.environ.get('CHAIN', 'external')
    return project.get_chain(chain_name)


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


def get_chain():
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),
             '..', '..', 'core'))
    project = Project()
    chain_name = os.environ.get('CHAIN', 'external')
    return project.get_chain(chain_name)
