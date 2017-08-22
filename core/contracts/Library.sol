pragma solidity ^0.4.2;

import "./Cartridge.sol";

contract Library {

    struct CartridgeCopy {
        address publisher;
        bytes32 signature;
    }

    CartridgeCopy[] cartridge_list;

    function list() public returns (address[] memory _list) {
        _list = new address[](cartridge_list.length);
        for (uint i = 0; i < cartridge_list.length; i++) {
            _list[i] = cartridge_list[i].publisher;
        }
    }

    function add(address publisher, bytes32 signature) public {
        require(Cartridge(publisher).validCopy(address(this)));
        cartridge_list.push(CartridgeCopy({
            publisher: publisher,
            signature: signature
        }));
    }
}
