pragma solidity ^0.4.19;

import "./zombiefactory.sol";

// 크립토키티 컨트랙트와 상호작용하기 위해 인터페이스를 정의한다 
contract KittyInterface {
  function getKitty(uint256 _id) external view returns (
    bool isGestating,
    bool isReady,
    uint256 cooldownIndex,
    uint256 nextActionAt,
    uint256 siringWithId,
    uint256 birthTime,
    uint256 matronId,
    uint256 sireId,
    uint256 generation,
    uint256 genes
  );
}


// ZombieFactory를 상속한 컨트랙트
contract zombieFeedig is ZombieFactory {

    // 크립토키티 인터페이스 생성 
    KittyInterface kittyContract;

    // 크립토키티 컨트랙트에 문제가 생기면 해당 주소를 바꾸기 위한 함수 
    // onlyOwner 제어자로 오직 이 컨트랙트의 소유자만 호출할 수 있게 한다 
    function setKittyContractAddress(address _address) external onlyOwner {
        kittyContract = KittyInterface(_address);
    }

    function _triggerCooldown(Zombie storage _zombie) internal {
        _zombie.readyTime = uint32(now + cooldownTime);
    }

    function _isReady(Zombie storage _zombie) internal view returns (bool) {
        return (_zombie.readyTime <= now);
    }

    function feedAndMultiply(uint _zombieId, uint _targetDna, string _species) internal {
        // 먹이를 주는 함수를 호출한 것이 좀비의 주인인지 확인한다. 
        require(msg.sender == zombieToOwner[_zombieId]);
        // 변수 myZombie는 블록체인 상에 영구적으로 저장된다 
        Zombie storage myZombie = zombies[_zombieId];
        // 쿨타임을 확인한다
        require(_isReady(myZombie));
        // 먹이의 dna가 16자리가 넘지 않도록 한다
        _targetDna = _targetDna % dnaModulus;
        // 좀비와 먹이의 dna의 평균을 새 dna로 정의한다 
        uint newDna = (myZombie.dna + _targetDna) / 2;
        // 종이 키티면 dna 마지막 2자리가 99로 끝나도록 만든다
        if (keccak256(_species) == keccak256("kitty")) {
            newDna = newDna - newDna % 100 + 99;
        }
        // 새 dna로 좀비를 만든다 
        _createZombie("NoName", newDna);
        // 쿨타임을 리셋한다
        _triggerCooldown(myZombie);
    }

    function feedOnKitty(uint _zombieId, uint _kittyId) public {
        uint kittyDna;
        // 크립토키티 컨트랙트에서 키티 유전자를 가져온다 
        (,,,,,,,,,kittyDna) = kittyContract.getKitty(_kittyId);
        // 키티 유전자를 좀비에게 먹이로 주어 새로운 좀비를 만든다 
        feedAndMultiply(_zombieId, kittyDna, "kitty");
    }
}