from amaranth.sim import Simulator, Delay, Settle
from nutty.units.constants import MemOP
from amaranth import *


class LSU(Elaboratable):
    def __init__(self) -> None:
        self.addr_i = Signal(32)
        self.data_i = Signal(32)
        self.data_o = Signal(32)
        self.lsu_op_i = Signal(8)  # one of 8 load / store ops
        self.mem_done_o = Signal()
        self.mem_load_done_o = Signal()
        self.mem_store_done_o = Signal()
        self.in_memory_transaction = Signal()
        # interface to memory bus
        self.data_mem_addr_o = Signal(32)
        self.data_mem_read_valid_i = Signal()
        self.data_mem_read_ready_o = Signal()
        self.data_mem_read_data_i = Signal(32)
        self.data_mem_write_valid_o = Signal()
        self.data_mem_write_ready_i = Signal()
        self.data_mem_write_data_o = Signal(32)
        self.data_mem_write_mask_o = Signal(4)

    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.data_mem_addr_o.eq(self.addr_i)
        is_load = Signal()
        is_store = Signal()  # tough could be derived from is_load but let's keep it to trace bugs
        m.d.comb += is_load.eq(self.lsu_op_i[0:5].any())
        m.d.comb += is_store.eq(self.lsu_op_i[5:8].any())
        with m.If(self.in_memory_transaction):
            with m.Switch(self.lsu_op_i):
                with m.Case(MemOP.LB, MemOP.LBU):  # LB, LBU
                    m.d.comb += self.data_mem_write_mask_o.eq(0)
                    m.d.sync += self.data_mem_write_valid_o.eq(0)

                    lb = Signal(8)
                    m.d.comb += self.mem_load_done_o.eq(0)
                    m.d.sync += self.data_mem_read_ready_o.eq(1)
                    with m.If(self.data_mem_read_valid_i):
                        m.d.sync += self.data_mem_read_ready_o.eq(0)
                        m.d.comb += self.mem_load_done_o.eq(1)
                        for i in range(4):  # other language generate pattern
                            with m.Switch(self.addr_i[0:2]):
                                with m.Case(i):
                                    m.d.comb += lb.eq(
                                        self.data_mem_read_data_i[i*8:(i+1)*8])
                        with m.If(self.lsu_op_i == 1):  # LB
                            # In Cat don't forget to make an array
                            m.d.sync += self.data_o.eq(Cat(lb, 24*[lb[-1]]))
                        with m.Else():  # LBU
                            m.d.sync += self.data_o.eq(Cat(lb, 24*[0]))

                with m.Case(MemOP.LH, MemOP.LHU):  # LH, #LHU
                    m.d.comb += self.data_mem_write_mask_o.eq(0)
                    m.d.sync += self.data_mem_write_valid_o.eq(0)
                    m.d.comb += self.mem_load_done_o.eq(0)
                    m.d.sync += self.data_mem_read_ready_o.eq(1)
                    with m.If(self.data_mem_read_valid_i):
                        m.d.sync += self.data_mem_read_ready_o.eq(0)
                        lh = Signal(16)
                        m.d.comb += self.mem_load_done_o.eq(1)
                        with m.Switch(self.addr_i[0:2]):
                            with m.Case(0):
                                m.d.comb += lh.eq(self.data_mem_read_data_i[0:16])
                            with m.Case(2):
                                m.d.comb += lh.eq(
                                    self.data_mem_read_data_i[16: 32])
                        with m.If(self.lsu_op_i == 2):  # LH
                            m.d.sync += self.data_o.eq(Cat(lh, 16*[lh[-1]]))
                        with m.Else():  # LHU
                            m.d.sync += self.data_o.eq(Cat(lh, 16*[0]))

                with m.Case(MemOP.LW):  # LW
                    m.d.comb += self.data_mem_write_mask_o.eq(0)
                    m.d.sync += self.data_mem_write_valid_o.eq(0)
                    m.d.comb += self.mem_load_done_o.eq(0)
                    m.d.sync += self.data_mem_read_ready_o.eq(1)
                    with m.If(self.data_mem_read_valid_i):
                        m.d.sync += self.data_mem_read_ready_o.eq(0)
                        m.d.comb += self.mem_load_done_o.eq(1)
                        m.d.sync += self.data_o.eq(self.data_mem_read_data_i)
                with m.Case(MemOP.SB):  # SB
                    with m.If(~self.data_mem_write_valid_o):
                        m.d.sync += self.data_mem_write_valid_o.eq(1)
                    with m.If(self.data_mem_write_ready_i & self.data_mem_write_valid_o):
                        m.d.sync += self.data_mem_write_valid_o.eq(0)
                        m.d.comb += self.mem_store_done_o.eq(1)
                    with m.Else():
                        m.d.comb += self.mem_store_done_o.eq(0)
                    sb = Signal(8)
                    m.d.comb += sb.eq(self.data_i[0:8])
                    with m.Switch(self.addr_i[0:2]):
                        with m.Case(0):
                            m.d.comb += self.data_mem_write_mask_o.eq(0b0001)
                            m.d.comb += self.data_mem_write_data_o.eq(
                                Cat(sb, 24*[0]))
                        with m.Case(1):
                            m.d.comb += self.data_mem_write_mask_o.eq(0b0010)
                            m.d.comb += self.data_mem_write_data_o.eq(
                                Cat(8*[0], sb, 16*[0]))
                        with m.Case(2):
                            m.d.comb += self.data_mem_write_mask_o.eq(0b0100)
                            m.d.comb += self.data_mem_write_data_o.eq(
                                Cat(16*[0], sb, 8*[0]))
                        with m.Case(3):
                            m.d.comb += self.data_mem_write_mask_o.eq(0b1000)
                            m.d.comb += self.data_mem_write_data_o.eq(
                                Cat(24*[0], sb))
                with m.Case(MemOP.SH):  # SH
                    with m.If(~self.data_mem_write_valid_o):
                        m.d.sync += self.data_mem_write_valid_o.eq(1)
                    with m.If(self.data_mem_write_ready_i & self.data_mem_write_valid_o):
                        m.d.sync += self.data_mem_write_valid_o.eq(0)
                        m.d.comb += self.mem_store_done_o.eq(1)
                    with m.Else():
                        m.d.comb += self.mem_store_done_o.eq(0)
                    sh = Signal(16)
                    m.d.comb += sh.eq(self.data_i[0:16])
                    with m.Switch(self.addr_i[0:2]):
                        with m.Case(0):
                            m.d.comb += self.data_mem_write_data_o.eq(
                                Cat(sh, 16*[0]))
                            m.d.comb += self.data_mem_write_mask_o.eq(0b0011)

                        with m.Case(2):
                            m.d.comb += self.data_mem_write_data_o.eq(
                                Cat(16*[0], sh))
                            m.d.comb += self.data_mem_write_mask_o.eq(0b1100)
                with m.Case(MemOP.SW):  # SW
                    m.d.comb += self.data_mem_write_data_o.eq(self.data_i)
                    m.d.comb += self.data_mem_write_mask_o.eq(0b1111)
                    with m.If(~self.data_mem_write_valid_o):
                        m.d.sync += self.data_mem_write_valid_o.eq(1)
                    with m.If(self.data_mem_write_ready_i & self.data_mem_write_valid_o):
                        m.d.sync += self.data_mem_write_valid_o.eq(0)
                        m.d.comb += self.mem_store_done_o.eq(1)
                    with m.Else():
                        m.d.comb += self.mem_store_done_o.eq(0)

                with m.Default():
                    m.d.sync += self.data_mem_write_valid_o.eq(0)
                    m.d.comb += self.data_mem_write_mask_o.eq(0)
                    m.d.comb += self.mem_load_done_o.eq(0)
                    m.d.comb += self.mem_store_done_o.eq(0)
                    m.d.sync += self.data_mem_read_ready_o.eq(0)
        m.d.comb += self.mem_done_o.eq(self.mem_store_done_o |  self.mem_load_done_o)
        return m


if __name__ == "__main__":
    dut = LSU()
    clk_period = 1e-6

    def test_case():
        while True:
            yield dut.lsu_op_i.eq(1)
            yield dut.data_mem_read_data_i.eq(0xdeadbeef)
            yield dut.data_mem_read_ready_o.eq(1)
            yield Delay(clk_period)
            yield dut.data_mem_read_valid_i.eq(1)
            yield Settle()
    sim = Simulator(dut)
    sim.add_process(test_case)
    with sim.write_vcd("lsu.vcd"):
        sim.run_until(10*clk_period)
