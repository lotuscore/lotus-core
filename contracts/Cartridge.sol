pragma solidity ^0.4.18;

import "zeppelin-solidity/contracts/ownership/Ownable.sol";
import "./Game.sol";

contract Cartridge is Ownable {
    Game public game;
    bytes public signature;
    address public originalOwner;
    string data;

    struct Endorsement {
        address owner;
        address newOwner;
        bytes signature;
    }

    Endorsement[] public endorsements;

    function Cartridge(address _owner, bytes _signature) public {
        game = Game(msg.sender);
        originalOwner = _owner;
        owner = _owner;
        signature = _signature;
    }

    function getData() public view returns (string) {
        require(msg.sender == owner || msg.sender == address(game.publisher));
        return data;
    }

    /**
    * @dev Allows the current owner to transfer control of the cartridge to a newOwner.
    * @param newOwner The address to transfer ownership to.
    * @param endorsement The newOwner address signed by the cartridge owner.
    */
    function transferOwnership(address newOwner, bytes endorsement) onlyOwner public {
        // require(validSignature(owner, newOwner, endorsement))
        endorsements.push(Endorsement(owner, newOwner, endorsement));
        return super.transferOwnership(newOwner);
    }

}
