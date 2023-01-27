from nutty.units.nutty_wb_soc import SoC
from amaranth_boards import arty_a7

if __name__ == "__main__":
    platform = arty_a7.ArtyA7_35Platform()
    led_pins = [platform.request("led", 0), platform.request(
        "led", 1), platform.request("led", 2), platform.request("led", 3)]
    arty_a7.ArtyA7_100Platform.add_clock_constraint(25e6)
    soc = SoC(led_pins)
    platform.build(soc, do_program=True)