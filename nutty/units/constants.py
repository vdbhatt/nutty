from amaranth import Const
from enum import Enum


class MemOP(Enum):
    LB = 1
    LBU = 8
    LH = 2
    LHU = 16
    LW = 4
    SB = 32
    SH = 64
    SW = 128


class Instr(Enum):
    LUI = 0
    AUIPC = 1
    JAL = 2
    JALR = 3
    BEQ = 4
    BNE = 5
    BLT = 6
    BGE = 7
    BLTU = 8
    BGEU = 9
    LB = 10
    LH = 11
    LW = 12
    LBU = 13
    LHU = 14
    SB = 15
    SH = 16
    SW = 17
    ADDI = 18
    SLTI = 19
    SLTIU = 20
    XORI = 21
    ORI = 22
    ANDI = 23
    SLLI = 24
    SRLI = 25
    SRAI = 26
    ADD = 27
    SUB = 28
    SLL = 29
    SLT = 30
    SLTU = 31
    XOR = 32
    SRL = 33
    SRA = 34
    OR = 35
    AND = 36
    FENCE = 37
    CSRRW = 38
    CSRRS = 39
    CSRRC = 40
    CSRRWI = 41
    CSRRSI = 42
    CSRRCI = 43
    UNKNOWN = 43


class InstType(Enum):
    """
    even tough the slice is taken lsb as 0th index the value
    is compared after composing the number
    so if bit array is 0101 -> 5 .
    Remember this in slicing.
    """

    LUI = 0b0110111
    AUIPC = 0b0010111
    JAL = 0b1101111
    JALR = 0b1100111
    BRANCH = 0b1100011
    LOAD = 0b0000011
    STORE = 0b0100011
    IMM = 0b0010011
    R = 0b0110011
    FENCE = 0b0001111
    SYSTEM = 0b1110011
