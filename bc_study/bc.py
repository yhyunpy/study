import time
import json
import hashlib
from urllib.parse import urlparse
import requests

from bc_model import *


class Blockchain(object):
    def __init__(self):
        self.chain: list[Block] = []
        self.current_transactions: list[Transaction] = []
        # 첫번째 블록체인
        self.new_block(previous_hash="1", proof=100)
        # 노드 목록
        self.nodes = set()

    def new_block(self, proof: int, previous_hash=None) -> Block:
        """
        블록체인에 새로운 블록체인을 만든다
        proof : 작업 증명 알고리즘이 제공하는 증명
        previous_hash : 이전 블록의 해시
        """
        block = Block(
            index=len(self.chain) + 1,
            timestamp=int(time.time()),
            transeactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash or self.hash(self.chain[-1]),
        )
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        """
        다음 채굴 블록으로 가기 위한 새로운 거래를 생성한다
        sender: 송신자의 주소
        recipient : 수신자의 주소
        amount: 양
        """
        self.current_transactions.append(
            Transaction(sender=sender, recipient=recipient, amount=amount)
        )
        return self.last_block.index + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block: Block) -> str:
        """
        블록의 해시를 만든다
        """
        block_dict = block.model_dump()
        block_string = json.dumps(block_dict, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof: int):
        """
        간단한 작업 증명
        - hash(pp')가 0000으로 시작하는 숫자 p'를 구하라.
        - p는 이전 증명이고 p'는 새로운 증명이다.
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        """
        증명을 검증한다
        """
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def register_node(self, address: str):
        """
        노드 리스트에 새 노드를 추가한다
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain: list[Block]):
        """
        블록체인이 유효한지 확인한다
        """
        previous_block = chain[0]
        now_idx = 1

        while now_idx < len(chain):
            now_block = chain[now_idx]
            if now_block.previous_hash != self.hash(previous_block):
                return False
            if not self.valid_proof(previous_block.proof, now_block.proof):
                return False
            previous_block = now_block
            now_idx += 1
        return True

    def resolve_conflicts(self):
        """
        합의 알고리즘.
        네트워크에서 가장 긴 체인으로 체인을 대체햐여 충돌을 해결한다
        """
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)

        # 네트워크에서 가장 긴 체인 찾기
        for node in neighbours:
            res = requests.get(f"http://{node}/chain")
            if res.status_code == 200:
                chain_res = ChainRes.parse_obj(res.json())
                length = chain_res.length
                chain = chain_res.chain
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # 가장 긴 체인으로 내 체인을 대체
        if new_chain:
            self.chain = new_chain
            return True

        return False
