import socket
import struct

from typing_extensions import Self

from .base import NetworkPacket


class ICMPPacket(NetworkPacket):

    def __init__(self,
                 type: int,
                 code: int,
                 checksum: int):
        self.type = type
        self.code = code
        self.checksum = checksum

    @classmethod
    def parse(cls, packet: bytes):
        format = "B B H"
        type, code, checksum = struct.unpack(format, packet)
        return cls(type=type,
                   code=code,
                   checksum=socket.htons(checksum))

class ICMPEchoReplyPacket(ICMPPacket):

    def __init__(self,
                 type: int,
                 code: int,
                 checksum: int,
                 identifier: int,
                 sequence: int,
                 data: bytes):
        super().__init__(type=type,
                         code=code,
                         checksum=checksum)
        self.identifier = identifier
        self.sequence = sequence
        self.data = data

    def __repr__(self):
        return (
                f"<{self.__class__.__name__} "
                f"type={self.type} code={self.code} "
                f"checksum={hex(self.checksum)}>"
        )

    @classmethod
    def parse(cls, packet: bytes) -> Self:
        format = "B B H H H"
        (
         type,
         code,
         checksum,
         id,
         seq
        ) = struct.unpack(format, packet[:struct.calcsize(format)])
        data = packet[struct.calcsize(format):]
        return cls(type=type,
                   code=code,
                   checksum=socket.htons(checksum),
                   identifier=id,
                   sequence=seq,
                   data=data)

class ICMPEchoPacket(ICMPEchoReplyPacket):
    ...

class ICMPReplyPacket(ICMPEchoReplyPacket):
    ...
