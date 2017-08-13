pragma solidity ^0.4.2;

contract Library {

    struct Cartridge {
        address publisher;
        bytes32 signature;
    }

    Cartridge[] user_library;

    function add(address publisher, bytes32 signature) {
        user_library.push(Cartridge({
            publisher: publisher,
            signature: signature
        }));
    }
}
