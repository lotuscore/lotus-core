import os

try:
    from db import DB, Settings
except ImportError:
    from app.db import DB, Settings  # exception occurs when deploy
from populus import Project
from populus.utils.wait import wait_for_transaction_receipt
from web3 import Web3

db = DB()


def get_settings():
    return db.session.query(Settings).first()


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


def touch_library():
    settings = get_settings()
    if settings.library_address:
        return

    with get_chain() as chain:
        Library = chain.provider.get_contract_factory('Library')
        web3 = chain.web3
        beneficiary = web3.eth.accounts[1]
        assert beneficiary
        txhash = Library.deploy(transaction={
            "from": beneficiary
        })
        receipt = check_succesful_tx(web3, txhash)
        library_address = receipt['contractAddress']
        settings.library_address = library_address
        db.session.commit()
