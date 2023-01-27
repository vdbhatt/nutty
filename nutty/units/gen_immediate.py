from amaranth import Elaboratable, Signal, signed, Module, Cat, Const
from enum import Enum
from nutty.units.constants import InstType


class GenImmediate(Elaboratable):
    def __init__(self) -> None:
        self.instr_i = Signal(32)
        self.immediate_o = Signal(32)

    def elaborate(self, platform):
        m = Module()
        with m.Switch((self.instr_i[0:7])):
            with m.Case(InstType.LUI, InstType.AUIPC):
                m.d.comb += self.immediate_o.eq(
                    Cat(Const(0, 12), self.instr_i[12:]))
            with m.Case(InstType.LOAD, InstType.JALR, InstType.IMM):
                m.d.comb += self.immediate_o.eq(
                    Cat(self.instr_i[20:32], 20*[self.instr_i[31]]))
            with m.Case(InstType.STORE):
                m.d.comb += self.immediate_o.eq(
                    Cat(self.instr_i[7:12],
                        self.instr_i[25:32], 20*[self.instr_i[31]])
                )
            with m.Case(InstType.BRANCH):
                m.d.comb += self.immediate_o.eq(
                    Cat(Const(0, 1), self.instr_i[8:12], self.instr_i[25:31],
                        self.instr_i[7], self.instr_i[31], 19*[self.instr_i[31]])
                )
            with m.Case(InstType.JAL):
                m.d.comb += self.immediate_o.eq(Cat(Const(
                    0, 1), self.instr_i[21:31], self.instr_i[20], self.instr_i[12:20], 12*[self.instr_i[31]]))
            with m.Default():
                m.d.comb += self.immediate_o.eq(0)
        return m
