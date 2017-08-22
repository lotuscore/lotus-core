from ethereum.tester import TransactionFailed

from conftest import CARTRIDGE_NAME, CARTRIDGE_PRICE


def test_cartridge_get_name(cartridge):
    cartridge_name = cartridge.call().getName()
    assert cartridge_name == CARTRIDGE_NAME


def test_buy_cartridge_success(cartridge, library):
    initial_list = library.call().list()
    cartridge.transact({'value': CARTRIDGE_PRICE}).buy(library.address)
    final_list = library.call().list()
    assert len(initial_list) + 1 == len(final_list)


def test_buy_cartridge_fail(cartridge, library):
    initial_list = library.call().list()
    try:
        cartridge.transact(
            {'value': CARTRIDGE_PRICE - 1}).buy(library.address)
    except TransactionFailed:
        pass
    else:
        assert False
    final_list = library.call().list()
    assert len(initial_list) == len(final_list)
