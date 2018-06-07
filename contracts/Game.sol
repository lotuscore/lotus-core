pragma solidity ^0.4.18;

import "zeppelin-solidity/contracts/ownership/Ownable.sol";
import "zeppelin-solidity/contracts/token/ERC20/ERC20.sol";
import "zeppelin-solidity/contracts/math/SafeMath.sol";
import "./Cartridge.sol";

contract Game is Ownable {
    using SafeMath for uint256;
    string public title;
    string public projectUrl;

    /*
     * 0000  Game
     * 0001  Game mod
     * 0010  Physical game
     * 0011  Soundtrack
     * 0100  Tool
     * 0101  Comic
     * 0110  Book
     */
    bytes1 public classification;

    /*
     * 0000  Released
     * 0001  In development
     * 0010  Canceled
     * 0011  Prototype
     */
    bytes1 public status;

    /*
     * Price in selected token or ETH if there is not.
     */
    uint256 public price;

    /*
     *  0000 No genre
     *  0001 Action
     *  0010 Adventure
     *  0011 Card Game
     *  0100 Educational
     *  0101 Fighting
     *  0110 Massively Multiplayer Online
     *  0111 Platformer
     *  1000 Puzzle
     *  1001 Racing
     *  1010 Rhythm
     *  1011 Role Playing
     *  1100 Shooter
     *  1101 Simulation
     *  1110 Sports
     *  1111 Strategy
     */
    bytes1 public genre;

    bytes16[] public tags;

    /*
     * Based on International Age Rating Coalition (IARC), the rating is
     * the sum of the minimum required age plus:
     * 00010000 for aimed at young audiences / All ages may play / Exempt / Not rated / No applicable rating.
     * 00100000 for parental guidance is suggested for designated age range.
     * 00110000 for not recommended for a younger audience but not restricted.
     * 01000000 for parental supervision required for younger audiences.
     * 01010000 for exclusively for older audience / Purchase age-restricted / Banned.
     */
    bytes1 public rating;

    /*
     * Available platforms is determined by the sum of the different alternatives
     * 00001 Windows
     * 00010 OSX
     * 00100 Linux
     * 01000 Android
     * 10000 iOS
     */
    bytes32 public platforms;

    /*
     * Download URL / Magnet Link / Game URL
     */
    string public data;

    /*
     * If signGuard is true the Cartridge will wait for the signature of the
     * publisher to be valid
     */
    bool public signGuard;

    address public publisher;

    /*
     * Token to be used to buy the Cartridge, if it is zero then
     * ethers will be used instead
     */
    ERC20 public token;

    mapping(address => uint8) public pendingPurchases;

    event CartridgeCreated(address owner);

    function Game(
        string _title,
        string _projectUrl,
        bytes1 _classification,
        bytes1 _status,
        uint256 _price,
        bytes1 _genre,
        bytes16[] _tags,
        bytes1 _rating,
        bytes32 _platforms,
        string _data,
        bool _signGuard,
        address _publisher,
        ERC20 _token
    ) public {
        title = _title;
        projectUrl = _projectUrl;
        classification = _classification;
        status = _status;
        price = _price;
        genre = _genre;
        tags = _tags;
        rating = _rating;
        platforms = _platforms;
        data = _data;
        signGuard = _signGuard;
        publisher = _publisher;
        token = _token;
    }


    function buyGame() public payable {
        require(_minimumPrice());

        uint256 allowance = address(token) == address(0) ? 0 : token.allowance(msg.sender, address(this));

        if (allowance > 0) {
            token.transferFrom(msg.sender, publisher, allowance);
        }
        if (msg.value > 0) {
            publisher.transfer(msg.value);
        }

        _createCartridge();
    }

    function _minimumPrice() internal view returns (bool) {
        if (price == 0) {
            return true;
        }
        if (address(token) == address(0)) {
            return msg.value >= price;
        }
        return token.allowance(msg.sender, address(this)) >= price;
    }

    function _createCartridge() internal {
        if (signGuard) {
            pendingPurchases[msg.sender]++;
        }
        else {
            new Cartridge(msg.sender, '');
            emit CartridgeCreated(msg.sender);
        }
    }

    function () external payable {
        buyGame();
    }

    function generate(address buyer, bytes signature) onlyOwner public {
        // require(validSignature(owner, buyer, signature))
        new Cartridge(buyer, signature);
        emit CartridgeCreated(buyer);
        if (pendingPurchases[buyer] > 0) {
            pendingPurchases[buyer]--;
        }
    }
}
