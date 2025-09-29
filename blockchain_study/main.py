from uuid import uuid4
from fastapi import FastAPI, HTTPException
from pydantic import AnyHttpUrl

from bc import Blockchain
from bc_model import *

app = FastAPI()

# 이 노드의 고유 주소
node_identifier = str(uuid4()).replace("-", "")

# 블록체인 인스턴스
blockchain = Blockchain()


# api
@app.get("/mine", description="새로운 블록을 만들어 코인 리워드를 받는다")
def get_mine():
    # 작업 증명
    last_block = blockchain.last_block
    last_proof = last_block.proof
    proof = blockchain.proof_of_work(last_proof)

    # 리워드 받기
    # sender가 "0"이면 이 노드가 새 코인을 채굴했다는 것을 뜻한다
    blockchain.new_transaction(sender="0", recipient=node_identifier, amount=1)

    # 새 블록 만들기
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof=proof, previous_hash=previous_hash)

    return block


@app.post("/transactions/new", description="새로운 거래를 생성한다")
def post_transactions_new(req: Transaction):
    return blockchain.new_transaction(req.sender, req.recipient, req.amount)


@app.get("/chain", description="블록체인을 조회한다")
def get_chain():
    return ChainRes(
        chain=blockchain.chain, length=len(blockchain.chain), is_replaced=False
    )


@app.post(
    "/nodes/register", description="url 형식의 주소 목록을 블록체인 노드로 등록한다"
)
def post_nodes_register(address_list: list[str]):
    if address_list == []:
        raise HTTPException(status_code=400)
    for address in address_list:
        blockchain.register_node(address)
    return list(blockchain.nodes)


@app.get(
    "/nodes/resolve",
    description="네트워크 내 다른 노드들과의 충돌을 해결하고 블록체인을 최신 상태로 교체한다",
)
def get_nodes_resolve():
    is_replaced = blockchain.resolve_conflicts()
    return ChainRes(
        chain=blockchain.chain, length=len(blockchain.chain), is_replaced=is_replaced
    )
