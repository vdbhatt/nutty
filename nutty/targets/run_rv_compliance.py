from nutty.units.nutty_wb_soc import SoC
from amaranth import *
from amaranth.cli import main
import argparse
import sys
import os
from nutty.utils.mem_utils import get_repo_path
if __name__ == "__main__":
    """
    Steps are as follows
    1. Build the firmware for given elf file and write the rom image in build folder
    2. Create the nutty_soc.v in build folder which will be used with the soc_verilog_tb.v by icarus verilog simulator to
    run the simulation. This hardware will have memory loaded
    3. launch the iverilog simulation, it will create the simulation_output.signature file in the build dir.
    4. copy the  simulation_output.signature to {sig} file
    """
    sys.setrecursionlimit(2**13)
    parser = argparse.ArgumentParser()
    parser.add_argument('--elf', help='elf file for the RISC-V test')
    parser.add_argument('--sig', help='destination for the signature')
    args = parser.parse_args()

    build_path = os.path.join(get_repo_path(),"test/riscof_work")
    elf_copy = os.path.join(build_path,args.sig.split('/')[-3]+ ".elf")
    image_rom =  os.path.join(build_path,"image.rom")
    compiled_soc = os.path.join(build_path,"compiled_soc")

    os.system(f"cp {args.elf} {elf_copy}")
    os.chdir(build_path)
    os.system(f"riscv32-unknown-elf-objdump -D {elf_copy} > {elf_copy}.objdump")
    os.system(f"riscv32-unknown-elf-objcopy -O binary {elf_copy} {elf_copy}.objcopy")
    os.system(f"hexdump -ve '1/4 \"%08x\n\"' {elf_copy}.objcopy > {image_rom}")

    # rom is built run vvp
    os.system(f"vvp {compiled_soc}")

    # at this point the simulation is run and the output text file should be available at the location given by the verilog testbench
    # now only thing remaining is to copy it to the signature location and we are done!
    output_filepath = os.path.join(build_path,"output.txt")
    os.system(f"cp {output_filepath} {args.sig}")