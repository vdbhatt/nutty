from amaranth import *
from amaranth_soc import wishbone
from amaranth_boards import arty_a7
from nutty.utils.mem_utils import read_memory_file
from nutty.units.nutty_wb import Nutty_WB
from lambdasoc.periph.sram import SRAMPeripheral
from nutty.units.led_peripheral import LEDPeripheral


class SoC(Elaboratable):
    def __init__(self, file_path,imem_size=16*1024,dmem_size=16*1024,led_pins=None,) -> None:
        self.nutty_wb = Nutty_WB()
        self.imem = SRAMPeripheral(size=imem_size, granularity=8)
        self.dmem = SRAMPeripheral(size=dmem_size, granularity=8)
        self.led = LEDPeripheral("led", base_addr=None,led_pins=led_pins)

        self._decoder = wishbone.Decoder(addr_width=32, data_width=32, granularity=8,name="dbus_decoder")

        self._arbiter = wishbone.Arbiter(addr_width=32,data_width=32,granularity=8)

        if file_path:
            self.imem.init = read_memory_file(file_path)
            self.dmem.init = read_memory_file(file_path)

        # this is hack to match the address when aligned with 4 bytes.
        # later need to fix it to do byte access
        self._decoder.add(self.dmem.bus, addr=0x80000000)
        self._decoder.add(self.imem.bus, addr=0x00000000)
        self._arbiter.add(self.nutty_wb.ibus)
        self._arbiter.add(self.nutty_wb.dbus)
        self._decoder.add(self.led.bus, addr=0x80004000)

    def elaborate(self, platform):
        m = Module()
        m.submodules.cpu = self.nutty_wb
        m.submodules.imem = self.imem
        m.submodules.dram = self.dmem
        m.submodules.led = self.led
        m.submodules.decoder = self._decoder
        m.submodules.arbiter = self._arbiter
        m.d.comb += self._arbiter.bus.connect(self._decoder.bus)
        return m


