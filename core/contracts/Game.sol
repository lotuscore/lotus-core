pragma solidity ^0.4.11;

import "zeppelin-solidity/contracts/ownership/Ownable.sol";
import "zeppelin-solidity/contracts/token/StandardToken.sol";
import "zeppelin-solidity/contracts/math/SafeMath.sol";
import "./Cartridge.sol";

contract Game is Ownable {
    using SafeMath for uint256;
    string name;
    bytes32 genre;
    bytes32 rating;
    uint16 platforms;
    uint256 price;
    bool signGuard;
    address publisher;
    StandardToken token;

    address[] pendingPurchases;

    event CartridgeCreated(address owner);

    function Game(string _name, bytes32 _genre, bytes32 _rating, uint16 _platforms, uint256 _price, bool _signGuard, address _publisher,  address _token) {
        name = _name;
        genre = _genre;
        rating = _rating;
        platforms = _platforms;
        price = _price;
        signGuard = _signGuard;
        publisher = _publisher;
        token = StandardToken(_token);
    }

    function buy(uint256 _value) {
        require(_value == price);
        token.transferFrom(msg.sender, publisher, _value);
        if (signGuard) {
            pendingPurchases.push(msg.sender);
        }
        else {
            new Cartridge(msg.sender, '');
            CartridgeCreated(msg.sender);
        }
    }

    function generate(address buyer, bytes signature) onlyOwner public {
        // require(validSignature(owner, buyer, signature))
        new Cartridge(buyer, signature);
        CartridgeCreated(buyer);
        for (uint256 i = 0; i < pendingPurchases.length; i++) {
            if (pendingPurchases[i] == buyer) {
                delete pendingPurchases[i];
                pendingPurchases[i] = pendingPurchases[pendingPurchases.length.sub(1)];
                pendingPurchases.length -= 1;
                break;
            }
        }
    }

}
