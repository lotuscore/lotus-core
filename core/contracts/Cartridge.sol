pragma solidity ^0.4.2;

import "./Library.sol";
import "./LotusToken.sol";

contract Cartridge {
    string name;
    bytes32 genre;
    bytes32 rating;
    uint platforms;
    uint256 price;

    function Cartridge(string _name, bytes32 _genre, bytes32 _rating, uint _platforms, uint256 _price) {
        name = _name;
        genre = _genre;
        rating = _rating;
        platforms = _platforms;
        price = _price;
    }

    function get_name() returns (string) {
        return name;
    }
}
