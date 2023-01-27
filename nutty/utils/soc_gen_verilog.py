from amaranth.cli import main
from amaranth import *
from nutty.units.nutty_wb_soc import SoC
from nutty.targets.config import imem_size, dmem_size
import os
if __name__ == "__main__":
    dut  = SoC(None,imem_size,dmem_size)
    sync = ClockDomain()
    m = Module()
    m.domains += sync
    m.submodules += dut
    main(m, ports=[sync.clk, sync.rst])