from dataclasses import dataclass, field
from decimal import Decimal
from eth_typing import HexStr, Hash32, Address
from typing import TypedDict, Union, NewType, Dict, Optional, List, Any
from hexbytes import HexBytes

ADDRESS_DEFAULT = HexStr("0x" + "0" * 40)

TokenAddress = NewType('token_address', HexStr)
TransactionHash = Union[Hash32, HexBytes, HexStr]
# L1WithdrawHash = Union[Hash32, HexBytes, HexStr]
L2WithdrawTxHash = Union[Hash32, HexBytes, HexStr]
From = NewType("from", int)
# Before = NewType('offset', int)
Limit = NewType('limit', int)


@dataclass
class Token:
    l1_address: HexStr
    l2_address: HexStr
    symbol: str
    decimals: int

    def format_token(self, amount) -> str:
        return str(Decimal(amount) / Decimal(10) ** self.decimals)

    def is_eth(self) -> bool:
        return self.l1_address == ADDRESS_DEFAULT and self.symbol == "ETH"

    def into_decimal(self, amount: int) -> Decimal:
        return Decimal(amount).scaleb(self.decimals) // Decimal(10) ** self.decimals

    def to_int(self, amount: Decimal) -> int:
        return int(amount * (Decimal(10) ** self.decimals))

    @staticmethod
    def create_eth() -> 'Token':
        return Token(ADDRESS_DEFAULT, ADDRESS_DEFAULT, "ETH", 18)


@dataclass
class Fee:
    feeToken: TokenAddress
    ergsLimit: int
    ergsPriceLimit: int
    ergsPerPubdataLimit: int

    @classmethod
    def default_fee(cls, address: TokenAddress) -> 'Fee':
        val = cls(feeToken=address,
                  ergsLimit=0,
                  ergsPriceLimit=0,
                  ergsPerPubdataLimit=0)
        return val


# TODO: check names, may be add field=meta for castings

@dataclass
class BridgeAddresses:
    l1_eth_default_bridge: HexStr
    l2_eth_default_bridge: HexStr
    l1_erc20_default_bridge: HexStr
    l2_erc20_default_bridge: HexStr


# TODO: implement corresponded types
VmExecutionSteps = NewType("VmExecutionSteps", Any)
ContractSourceDebugInfo = NewType("ContractSourceDebugInfo", Any)


@dataclass
class VmDebugTrace:
    steps: List[VmExecutionSteps]
    sources: Dict[str, ContractSourceDebugInfo]