pragma solidity ^0.4.2;

contract Library {

    struct Cartridge {
        address publisher;
        bytes32 signature;
    }

    Cartridge[] user_library;

    function list() public returns (address[] memory _list) {
        _list = new address[](user_library.length);
        for (uint i = 0; i < user_library.length; i++) {
            _list[i] = user_library[i].publisher;
        }
    }

    function add(address publisher, bytes32 signature) {
        user_library.push(Cartridge({
            publisher: publisher,
            signature: signature
        }));
    }
}
