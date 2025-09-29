from pydantic import BaseModel


class Block(BaseModel):
    index: int
    timestamp: int
    transeactions: list
    proof: int
    previous_hash: str | None = None


class Transaction(BaseModel):
    sender: str
    recipient: str
    amount: int


class ChainRes(BaseModel):
    chain: list[Block]
    length: int
    is_replaced: bool
