import socket
import struct

from ..utils import enforce_mac
from .base import DataLinkPacket


class EthernetPacket(DataLinkPacket):
    format = "6s 6s H"

    def __init__(self, src_addr: str, dest_addr: str, type: int):
        self.src_addr = src_addr
        self.dest_addr = dest_addr
        self.type = type

    def get_type(self):
        return self.type

    def __repr__(self):
        return (
            f"<EthernetPacket src_addr={self.src_addr}"
            f" dest_addr={self.dest_addr} type={self.type}>"
        )

    def __len__(self):
        return 14

    @classmethod
    def parse(cls, packet: bytes):
        ethernet_frame = packet[:14]
        src_addr, dest_addr, type = struct.unpack(cls.format, ethernet_frame)
        return cls(
            src_addr=enforce_mac(src_addr),
            dest_addr=enforce_mac(dest_addr),
            type=socket.htons(type),
        )
