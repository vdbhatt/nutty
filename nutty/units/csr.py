from amaranth import *

class CSR(Elaboratable):
    def __init__(self):
        self.wr_addr_i = Signal(range(4096))
        self.rd_addr_i = Signal(range(4096))
        self.data_in = Signal(32)
        self.write_en_i = Signal(32)
        self.data_o = Signal(32)

        self._mstatus = Signal(32)
        self._misa = Signal(32)
        self._medeleg = Signal(32)
        self._mideleg = Signal(32)
        self._mie = Signal(32)
        self._mtvec = Signal(32)
        self._mepc = Signal(32)
        self._mcause = Signal(32)
        self._mtval = Signal(32)
        self._mip = Signal(32)
        self._mtinst = Signal(32)
        self._mcycle = Signal(32)
        self._minstret = Signal(32)

    def elaborate(self,platform):
        m = Module()
        if m.If(self.write_en_i):
            with m.If(self.wr_addr_i == 0x300): # mstatus
                m.d.sync += self.mstatus.eq(self.data_in)
                m.d.sync += self.data_o.eq(self._mstatus)
            with m.If
        return m
