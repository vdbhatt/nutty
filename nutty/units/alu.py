from amaranth import Elaboratable, Signal, Module,signed


class ALU(Elaboratable):
    def __init__(self) -> None:
        self.op1_i = Signal(32)
        self.op2_i = Signal(32)
        self.control_i = Signal(5)
        self.result_o = Signal(32)

    def elaborate(self, platform):
        m = Module()
        signed_op1_i = Signal(signed(32))
        signed_op2_i = Signal(signed(32))
        m.d.comb += signed_op1_i.eq(self.op1_i)
        m.d.comb += signed_op2_i.eq(self.op2_i)
        with m.Switch(self.control_i):
            with m.Case(1):
                m.d.comb += self.result_o.eq(signed_op1_i + signed_op2_i)
            with m.Case(2):
                m.d.comb += self.result_o.eq(self.op2_i)
            with m.Case(3):
                m.d.comb += self.result_o.eq(signed_op1_i - signed_op2_i)
            with m.Case(4):
                with m.If(signed_op1_i < signed_op2_i):
                    m.d.comb += self.result_o.eq(1)
                with m.Else():
                    m.d.comb += self.result_o.eq(0)
            with m.Case(5):
                with m.If(self.op1_i < self.op2_i):
                    m.d.comb += self.result_o.eq(1)
                with m.Else():
                    m.d.comb += self.result_o.eq(0)
            with m.Case(6):
                m.d.comb += self.result_o.eq(self.op1_i ^ self.op2_i)
            with m.Case(7):
                m.d.comb += self.result_o.eq(self.op1_i | self.op2_i)
            with m.Case(8):
                m.d.comb += self.result_o.eq(self.op1_i & self.op2_i)
            with m.Case(9):
                m.d.comb += self.result_o.eq(self.op1_i << self.op2_i[:5])
            with m.Case(10):
                m.d.comb += self.result_o.eq(self.op1_i >> self.op2_i[:5])
            with m.Case(11):
                m.d.comb += self.result_o.eq(signed_op1_i >> signed_op2_i[:5])
            with m.Case():
                m.d.comb += self.result_o.eq(0xdeadbeef)
        return m
