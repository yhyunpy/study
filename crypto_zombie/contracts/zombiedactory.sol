pragma solidity ^0.4.19;

import "./ownable.sol";

contract ZombieFactory is Ownable{
    // 이벤트 선언
    event NewZombie(uint zimbieId, string name, uint dna);

    // 변수 선언
    uint dnaDigits = 16;
    uint dnaModulus = 10 ** dnaDigits;
    uint cooldownTime = 1 days;

    // 구조체 선언
    struct Zombie {
        string name;
        uint dna;
        uint32 level;
        uint32 readyTime;
    }

    // 배열 선언 
    Zombie[] public zombies;

    // 매핑 선언 
    mapping (uint => address) public zombieToOwner;
    mapping (address => uint) public ownerZombieCount;

    // internal로 선언하여 상속 컨트랙트에서도 접근 가능하도록 한다. 
    function _createZombie(string _name, uint _dna) internal {
        // 배열에 push 하면 새로운 배열의 길이가 리턴된다. 즉 배열의 인덱스를 새로운 좀비의 id로 부여한다. 
        uint id = zombies.push(Zombie(_name, _dna, 1, uint32(now _ cooldownTime))) - 1 ;
        // 좀비 id를 키로, 함수 호출자의 주소를 값으로 매핑한다. 
        zombieToOwner[id] = msg.sender;
        // 함수 호출자의 주소를 키로, 좀비 개수 카운트를 증가시킨다.  
        ownerZombieCount[msg.sender]++;
        // 이벤트를 실행한다.
        NewZimbie(id, _name, _dna);
    }

    function _generateRandomDna(string _str) private view returns (uint) {
        uint rand = uint(keccak256(_str));
        return rand % dnaModulus;
    }

    function createRandomZombie(string _name) public {
        // 함수 호출자가 소유한 좀비가 0개인지 확인한다. 
        require(ownerZombieCount[msg.sender] == 0);
        uint randDna = _generateRandomDna((_name));
        _createZombie(_name, randDna);
    }
}