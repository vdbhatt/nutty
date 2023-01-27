from amaranth import Elaboratable, Signal, Module, signed


class Branch(Elaboratable):
    def __init__(self):
        self.op1_i = Signal(32)
        self.op2_i = Signal(32)
        self.control_i = Signal(3)
        self.branch_taken_o = Signal()

    def elaborate(self, platform):
        m = Module()

        signed_op1 = Signal(signed(32))
        signed_op2 = Signal(signed(32))
        m.d.comb += signed_op1.eq(self.op1_i)
        m.d.comb += signed_op2.eq(self.op2_i)

        with m.Switch(self.control_i):
            with m.Case(0):
                m.d.comb += self.branch_taken_o.eq(0)
            with m.Case(1):
                with m.If(self.op1_i == self.op2_i):
                    m.d.comb += self.branch_taken_o.eq(1)
                with m.Else():
                    m.d.comb += self.branch_taken_o.eq(0)
            with m.Case(2):
                with m.If(self.op1_i != self.op2_i):
                    m.d.comb += self.branch_taken_o.eq(1)
                with m.Else():
                    m.d.comb += self.branch_taken_o.eq(0)

            with m.Case(3):
                with m.If(signed_op1 < signed_op2):
                    m.d.comb += self.branch_taken_o.eq(1)
                with m.Else():
                    m.d.comb += self.branch_taken_o.eq(0)
            with m.Case(4):
                with m.If(signed_op1 >= signed_op2):
                    m.d.comb += self.branch_taken_o.eq(1)
                with m.Else():
                    m.d.comb += self.branch_taken_o.eq(0)
            with m.Case(5):
                with m.If(self.op1_i < self.op2_i):
                    m.d.comb += self.branch_taken_o.eq(1)
                with m.Else():
                    m.d.comb += self.branch_taken_o.eq(0)
            with m.Case(6):
                with m.If(self.op1_i >= self.op2_i):
                    m.d.comb += self.branch_taken_o.eq(1)
                with m.Else():
                    m.d.comb += self.branch_taken_o.eq(0)
            with m.Case():
                m.d.comb += self.branch_taken_o.eq(0)
        return m
