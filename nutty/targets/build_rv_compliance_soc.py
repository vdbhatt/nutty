import argparse
import sys
import os
import re
from nutty.utils.mem_utils import get_repo_path
def build_rv_compliance_soc():
    repo = get_repo_path()
    build_path = os.path.join(repo,"test/riscof_work")
    generated_verilog_soc = os.path.join(build_path,"nutty_soc.v")
    generated_optimized_verilog_soc = os.path.join(build_path,"optimized_nutty_soc.v")
    python_gen_script = os.path.join(repo,"nutty/utils/soc_gen_verilog.py")
    os.system(f"python {python_gen_script} generate -t v > {generated_verilog_soc} ")
    out_lines = []
    for line in open(generated_verilog_soc):
        if not re.match(r"[\s]*[_mem]*[\[]([0-9]{3,})]\s[=\s32'd0;]*",line):
            out_lines.append(line)
        # if not re.match(r"\s*\breg\s\[31:0]\s_mem\s\[63:0];",line):
        #     out_lines.append(line)
        # else:
        #     print( line)
        #     out_lines.append(f"reg [31:0] _mem [{mem_length-1}:0];")
    with open(generated_optimized_verilog_soc,"w") as f:
        f.writelines(out_lines)
    verilog_tb = os.path.join(repo,"test/rv_compliance/soc_verilog_tb.v")
    compiled_soc = os.path.join(build_path,"compiled_soc")
    os.system(f"iverilog -o {compiled_soc} {generated_optimized_verilog_soc} {verilog_tb} ")

if __name__ == "__main__":
    build_rv_compliance_soc()