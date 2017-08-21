def test_cartridge(chain):
    _cartridge_name = 'cartridge name'
    cartridge, _ = chain.provider.get_or_deploy_contract(
        'Cartridge', deploy_args=[_cartridge_name, 'genre', 'rating', 1, 1])

    cartridge_name = cartridge.call().get_name()
    assert cartridge_name == _cartridge_name
