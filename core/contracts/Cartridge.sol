pragma solidity ^0.4.2;

import "./Library.sol";
import "./LotusToken.sol";

contract Cartridge {
    string name;
    bytes32 genre;
    bytes32 rating;
    uint platforms;
    uint256 price;

    mapping(address => address) public copies;

    function Cartridge(string _name, bytes32 _genre, bytes32 _rating, uint _platforms, uint256 _price) {
        name = _name;
        genre = _genre;
        rating = _rating;
        platforms = _platforms;
        price = _price;
    }

    function buy(Library libraryAddress) payable {
        require(msg.value >= price);
        copies[libraryAddress] = msg.sender;
        Library(libraryAddress).add(address(this), '');
    }

    function validCopy(address libraryAddress) returns (bool) {
        return copies[libraryAddress] != address(0x0);
    }

    function getName() returns (string) {
        return name;
    }
}
