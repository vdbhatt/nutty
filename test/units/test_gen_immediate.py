from amaranth.sim import Settle, Delay
from amaranth import Elaboratable, Signal, signed, Module, Cat, Const
from constants import InstType
from amaranth.sim import Simulator


from gen_immediate import GenImmediate

if __name__ == "__main__":
    dut = GenImmediate()

    def set_instr(value):
        yield dut.instr_i.eq(value)
        yield Settle()
        yield Delay(1e-6)

    def test_cases():
        yield from set_instr(Const(0xcc828293, 32))

    sim = Simulator(dut)
    sim.add_process(test_cases)
    with sim.write_vcd("gen_imm.vcd"):
        sim.run()
