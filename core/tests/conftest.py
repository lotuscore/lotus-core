import pytest

CARTRIDGE_NAME = 'cartridge name'
CARTRIDGE_PRICE = 10


@pytest.fixture()
def cartridge(chain):
    cartridge, _ = chain.provider.get_or_deploy_contract(
        'Cartridge',
        deploy_args=[CARTRIDGE_NAME, 'genre', 'rating', 1, CARTRIDGE_PRICE])
    return cartridge


@pytest.fixture()
def library(chain):
    library, _ = chain.provider.get_or_deploy_contract('Library')
    return library
