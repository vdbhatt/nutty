from amaranth.sim import Simulator
from amaranth.sim import Delay, Settle
from amaranth import Elaboratable, Signal, Module, Const, Cat
from nutty.units.constants import InstType
from nutty.units.constants import Instr as I
from nutty.units.constants import *


class Decoder(Elaboratable):
    def __init__(self):
        self.instr_i = Signal(32)
        self.rd_o = Signal(5)
        self.rs1_o = Signal(5)
        self.rs2_o = Signal(5)
        self.opcode_o = Signal(7)
        self.illegal_instr = Signal()
        self.branch_type_o = Signal(3)
        self.branch_instr_o = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.rd_o.eq(self.instr_i[7:12])
        m.d.comb += self.rs1_o.eq(self.instr_i[15:20])
        m.d.comb += self.rs2_o.eq(self.instr_i[20:25])
        x = Signal(7)
        func3 = Signal(3)
        m.d.comb += func3.eq(self.instr_i[12:15])
        m.d.comb += x.eq(self.instr_i[0:7])
        with m.Switch((self.instr_i[0:7])):
            with m.Case(InstType.LUI):
                m.d.comb += self.opcode_o.eq(0)
            with m.Case(InstType.AUIPC):
                m.d.comb += self.opcode_o.eq(I.AUIPC)
            with m.Case(InstType.JAL):
                m.d.comb += self.opcode_o.eq(I.JAL)
            with m.Case(InstType.JALR):
                m.d.comb += self.opcode_o.eq(I.JALR)

            with m.Case(InstType.BRANCH):
                m.d.comb += self.branch_instr_o.eq(self.branch_type_o.any())
                with m.Switch(self.instr_i[12:15]):
                    with m.Case(0):
                        m.d.comb += self.opcode_o.eq(I.BEQ)
                        m.d.comb += self.branch_type_o.eq(1)
                    with m.Case(1):
                        m.d.comb += self.opcode_o.eq(I.BNE)
                        m.d.comb += self.branch_type_o.eq(2)
                    with m.Case(4):
                        m.d.comb += self.opcode_o.eq(I.BLT)
                        m.d.comb += self.branch_type_o.eq(3)
                    with m.Case(5):
                        m.d.comb += self.opcode_o.eq(I.BGE)
                        m.d.comb += self.branch_type_o.eq(4)
                    with m.Case(6):
                        m.d.comb += self.opcode_o.eq(I.BLTU)
                        m.d.comb += self.branch_type_o.eq(5)
                    with m.Case(7):
                        m.d.comb += self.opcode_o.eq(I.BGEU)
                        m.d.comb += self.branch_type_o.eq(6)
                    with m.Default():
                        m.d.comb += self.opcode_o.eq(I.UNKNOWN)
                        m.d.comb += self.branch_type_o.eq(0)
                        m.d.comb += self.branch_instr_o.eq(0)
            with m.Case(InstType.LOAD):
                with m.Switch(self.instr_i[12:15]):
                    with m.Case(0):
                        m.d.comb += self.opcode_o.eq(I.LB)
                    with m.Case(1):
                        m.d.comb += self.opcode_o.eq(I.LH)
                    with m.Case(2):
                        m.d.comb += self.opcode_o.eq(I.LW)
                    with m.Case(4):
                        m.d.comb += self.opcode_o.eq(I.LBU)
                    with m.Case(5):
                        m.d.comb += self.opcode_o.eq(I.LHU)
                    with m.Default():
                        m.d.comb += self.opcode_o.eq(I.UNKNOWN)
            with m.Case(InstType.STORE):
                with m.Switch(self.instr_i[12:15]):
                    with m.Case(0):
                        m.d.comb += self.opcode_o.eq(I.SB)
                    with m.Case(1):
                        m.d.comb += self.opcode_o.eq(I.SH)
                    with m.Case(2):
                        m.d.comb += self.opcode_o.eq(I.SW)
                    with m.Default():
                        m.d.comb += self.opcode_o.eq(I.UNKNOWN)
            with m.Case(InstType.IMM):
                with m.Switch((self.instr_i[12:15])):
                    with m.Case(0):
                        m.d.comb += self.opcode_o.eq(I.ADDI)
                    with m.Case(1):
                        m.d.comb += self.opcode_o.eq(I.SLLI)
                    with m.Case(2):
                        m.d.comb += self.opcode_o.eq(19)
                    with m.Case(3):
                        m.d.comb += self.opcode_o.eq(I.SLTIU)
                    with m.Case(4):
                        m.d.comb += self.opcode_o.eq(I.XORI)
                    with m.Case(5):
                        with m.Switch(self.instr_i[25:]):
                            with m.Case(0):
                                m.d.comb += self.opcode_o.eq(I.SRLI)
                            with m.Case(32):
                                m.d.comb += self.opcode_o.eq(I.SRAI)
                            with m.Default():
                                m.d.comb += self.opcode_o.eq(I.UNKNOWN)
                    with m.Case(6):
                        m.d.comb += self.opcode_o.eq(I.ORI)
                    with m.Case(7):
                        m.d.comb += self.opcode_o.eq(I.ANDI)
                    with m.Default():
                        m.d.comb += self.opcode_o.eq(I.UNKNOWN)
            with m.Case(InstType.R):
                with m.Switch(Cat(self.instr_i[12:15], self.instr_i[30])):
                    with m.Case(0):
                        m.d.comb += self.opcode_o.eq(I.ADD)
                    with m.Case(8):
                        m.d.comb += self.opcode_o.eq(I.SUB)
                    with m.Case(1):
                        m.d.comb += self.opcode_o.eq(I.SLL)
                    with m.Case(2):
                        m.d.comb += self.opcode_o.eq(I.SLT)
                    with m.Case(3):
                        m.d.comb += self.opcode_o.eq(I.SLTU)
                    with m.Case(4):
                        m.d.comb += self.opcode_o.eq(I.XOR)
                    with m.Case(5):
                        m.d.comb += self.opcode_o.eq(I.SRL)
                    with m.Case(13):
                        m.d.comb += self.opcode_o.eq(I.SRA)
                    with m.Case(6):
                        m.d.comb += self.opcode_o.eq(I.OR)
                    with m.Case(7):
                        m.d.comb += self.opcode_o.eq(I.AND)
                    with m.Default():
                        m.d.comb += self.opcode_o.eq(I.UNKNOWN)
            with m.Case(InstType.FENCE):
                m.d.comb += self.opcode_o.eq(I.FENCE)
            with m.Case(InstType.SYSTEM):

                with m.Switch(self.instr_i[12:15]):
                    with m.Case(0):
                        # ecall or ebreak o
                        with m.If(self.instr_i[20:] == 0):
                            pass
                    with m.Case(1):
                        m.d.comb += self.opcode_o.eq(I.CSRRW)
                        pass
                    with m.Case(2):
                        m.d.comb += self.opcode_o.eq(I.CSRRS)
                        pass
                    with m.Case(3):
                        m.d.comb += self.opcode_o.eq(I.CSRRC)
                        pass
                    with m.Case(5):
                        m.d.comb += self.opcode_o.eq(I.CSRRWI)
                        pass
                    with m.Case(6):
                        m.d.comb += self.opcode_o.eq(I.CSRRSI)
                        pass
                    with m.Case(7):
                        m.d.comb += self.opcode_o.eq(I.CSRRCI)
                        pass
            with m.Default():
                m.d.comb += self.opcode_o.eq(1)
                m.d.comb += self.illegal_instr.eq(1)
        return m


if __name__ == "__main__":
    dut = Decoder()

    def set_instr(value):
        yield dut.instr_i.eq(value)
        yield Settle()
        yield Delay(1e-6)

    def test_cases():
        yield from set_instr(Cat(Const(0xFF410113, 32)))

    sim = Simulator(dut)
    sim.add_process(test_cases)
    with sim.write_vcd("decoder.vcd"):
        sim.run()
