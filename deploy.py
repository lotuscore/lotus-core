"""Deploy Lotus token and smart contract.

A simple Python script to deploy contracts and then do a smoke test for them.
"""
import os

from populus import Project
from populus.utils.cli import get_unlocked_default_account_address

from app.db import DB, Settings
from app.utils import check_succesful_tx

db = DB()


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

        # update local database
        settings = db.session.query(Settings).first()
        settings.token_address = token_address
        db.session.commit()


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core'))
    main()
