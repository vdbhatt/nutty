from nutty.units.nutty_wb_soc import SoC
from amaranth.sim import Simulator
import sys

if __name__ == "__main__":
    sys.setrecursionlimit(2**13)
    unit_test_rom_image = r"/workspaces/amaranth_ws/amaranth_tutorial/risc_v/firmware/build/nutty.rom"
    dut = SoC(unit_test_rom_image,0x10,0x40)
    def test_process():
        while True:
            yield
    sim = Simulator(dut)
    sim.add_clock(1/1e6)
    sim.add_sync_process(test_process)

    with sim.write_vcd("nutty_soc.vcd"):
        sim.run_until(60e-6)
