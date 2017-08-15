pragma solidity ^0.4.2;

contract Library {

    struct Cartridge {
        address publisher;
        bytes32 signature;
    }

    Cartridge[] user_library;

    function list() returns (address[]) {
        address[] list;
        for (uint i = 1; i < user_library.length; i++) {
            list.push(user_library[i].publisher);
        }
        return list;
    }

    function add(address publisher, bytes32 signature) {
        user_library.push(Cartridge({
            publisher: publisher,
            signature: signature
        }));
    }
}
