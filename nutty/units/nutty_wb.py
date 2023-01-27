from amaranth import *
from amaranth_soc import wishbone
from nutty.units.nutty import Nutty

class Nutty_WB(Elaboratable):
    def __init__(self):
        self.nutty = Nutty()
        self.ibus = wishbone.Interface(
            addr_width=32, data_width=32, granularity=8, name="imem")
        self.dbus = wishbone.Interface(
            addr_width=32, data_width=32, granularity=8, name="dmem")

    def elaborate(self, platform):
        m = Module()
        m.submodules.nutty = nutty = self.nutty
        # instr bus
        m.d.comb += nutty.instr_mem_valid_i.eq(self.ibus.ack)
        with m.If(nutty.instr_mem_ready_o):
            m.d.comb += self.ibus.cyc.eq(1)
            m.d.comb += self.ibus.stb.eq(1)
            m.d.comb += self.ibus.we.eq(0)
            m.d.comb += self.ibus.adr.eq(nutty.instr_mem_addr_o)
            m.d.comb += self.ibus.sel.eq(15)

            with m.If(self.ibus.ack):
                m.d.comb += nutty.instr_mem_data_i.eq(self.ibus.dat_r)
                m.d.comb += self.ibus.stb.eq(0)
                m.d.comb += self.ibus.cyc.eq(0)
        # data bus
        # read
        m.d.comb += nutty.data_mem_read_valid_i.eq(self.dbus.ack)
        # m.d.comb += self.dbus.adr.eq(nutty.data_mem_addr_o)
        m.d.comb += self.dbus.adr.eq(Cat(nutty.data_mem_addr_o[2:],2*[0]))
        with m.If(nutty.data_mem_read_ready_o):
            m.d.comb += self.dbus.cyc.eq(1)
            m.d.comb += self.dbus.stb.eq(1)
            m.d.comb += self.dbus.we.eq(0)
            m.d.comb += self.dbus.sel.eq(15)
            with m.If(self.dbus.ack):
                m.d.comb += nutty.data_mem_data_i.eq(self.dbus.dat_r)
                m.d.comb += self.dbus.stb.eq(0)
                m.d.comb += self.dbus.cyc.eq(0)
        # write
        with m.If(nutty.data_mem_write_valid_o):
            m.d.comb += self.dbus.cyc.eq(1)
            m.d.comb += self.dbus.stb.eq(1)
            m.d.comb += self.dbus.we.eq(1)
            m.d.comb += self.dbus.sel.eq(nutty.data_mem_write_mask_o)
            m.d.comb += self.dbus.dat_w.eq(nutty.data_mem_data_o)
            m.d.comb += nutty.data_mem_write_ready_i.eq(0)
            with m.If(self.dbus.ack):
                m.d.comb += self.dbus.stb.eq(0)
                m.d.comb += self.dbus.cyc.eq(0)
                m.d.comb += nutty.data_mem_write_ready_i.eq(1)
        with m.Else():
            m.d.comb += nutty.data_mem_write_ready_i.eq(1)

        return m  # TODO:  remember to always return m else error is not easy to understand


