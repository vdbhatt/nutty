from amaranth import *
from lambdasoc.periph.base import Peripheral

class LEDPeripheral(Peripheral, Elaboratable):

    def __init__(self, name, *, base_addr, led_pins) -> None:
        super().__init__()
        self.name = name+"_peri_"
        self._csr_bank = self.csr_bank(name="_csr_bank")
        self.led_status = self._csr_bank.csr(
            32, "rw")#, addr=1)  # base_addr+1)
        self._bridge = self.bridge(data_width=32, granularity=8, alignment=0)
        self.bus = self._bridge.bus
        self.led_pins = led_pins

    def elaborate(self, platform):
        m = Module()
        m.submodules.peri_bridge = self._bridge

        led = Signal(32)
        with m.If(self.led_status.w_stb):  # write to leds
            m.d.sync += self.led_status.r_data.eq(self.led_status.w_data)
        m.d.comb += led.eq(self.led_status.w_data)
        if self.led_pins:
            m.d.comb += Cat([led_pin.o for led_pin in self.led_pins[:-1]]
                            ).eq(led[0:4])
            m.d.comb += self.led_pins[-1].o.eq(1)
            # attach the leds of platform to the status CSR

        return m
