def test_library(chain):
    library, _ = chain.provider.get_or_deploy_contract('Library')

    library.transact().add(
        publisher='0x89c2a280a483f45a3d140ef752ffe9c6cd4b57fa', signature='0')
    cartridge_list = library.call().list()
    assert len(cartridge_list) == 1
