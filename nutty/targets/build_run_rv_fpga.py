import argparse
import sys
import os
import re
from nutty.utils.mem_utils import get_repo_path
def build_rv_compliance_soc():
    repo = get_repo_path()
    make_path = os.path.join(repo,"test/sw")
    cwd = os.getcwd()
    os.chdir(make_path)
    os.system("make")
    os.chdir(cwd)
    build_path = os.path.join(repo,"test/fpga_work")
    generated_verilog_soc = os.path.join(build_path,"nutty_soc_fpga.v")
    generated_optimized_verilog_soc = os.path.join(build_path,"optimized_nutty_soc.v")
    python_gen_script = os.path.join(repo,"nutty/utils/soc_gen_verilog.py")
    os.system(f"python {python_gen_script} generate -t v > {generated_verilog_soc} ")
    out_lines = []
    for line in open(generated_verilog_soc):
        if not re.match(r"[\s]*[_mem]*[\[]([0-9]{3,})]\s[=\s32'd0;]*",line):
            out_lines.append(line)
    with open(generated_optimized_verilog_soc,"w") as f:
        f.writelines(out_lines)
    verilog_tb = os.path.join(repo,"test/sw/soc_verilog_tb_sim.v")
    compiled_soc = os.path.join(build_path,"compiled_soc")
    os.system(f"iverilog -o {compiled_soc} {generated_optimized_verilog_soc} {verilog_tb} ")
    os.system(f"vvp {compiled_soc}")

if __name__ == "__main__":
    build_rv_compliance_soc()