import os
from nutty.utils.mem_utils import get_repo_path

if not os.path.exists(os.path.join(get_repo_path(),"test/rv_compliance/riscv-arch-test")):
    os.chdir(os.path.join(get_repo_path(),"test/rv_compliance"))
    os.system("riscof --verbose info arch-test --clone")
test_suite = os.path.join(get_repo_path(),"test/rv_compliance/riscv-arch-test/riscv-test-suite/")
test_env = os.path.join(get_repo_path(),"test/rv_compliance/riscv-arch-test/riscv-test-suite/env")
work_dir = os.path.join(get_repo_path(),"test/riscof_work")
config_ini = os.path.join(get_repo_path(),"test/rv_compliance/nutty_plugin/config.ini")
# fix the paths in cofig.ini
with open(config_ini,'w') as f:
    f.writelines("[RISCOF]\n")
    f.writelines("ReferencePlugin=sail_cSim\n")
    f.writelines(f"ReferencePluginPath={get_repo_path()}/test/rv_compliance/nutty_plugin/sail_cSim\n")
    f.writelines(f"DUTPlugin=nutty\n")
    f.writelines(f"DUTPluginPath={get_repo_path()}/test/rv_compliance/nutty_plugin/nutty\n\n")
    f.writelines(f"[nutty]\n")
    f.writelines(f"pluginpath={get_repo_path()}/test/rv_compliance/nutty_plugin/nutty\n")
    f.writelines(f"ispec={get_repo_path()}/test/rv_compliance/nutty_plugin/nutty/nutty_isa.yaml\n")
    f.writelines(f"pspec={get_repo_path()}/test/rv_compliance/nutty_plugin/nutty/nutty_platform.yaml\n")
    f.writelines(f"target_run=1\n\n")
    f.writelines(f"[sail_cSim]\n")
    f.writelines(f"pluginpath={get_repo_path()}/test/rv_compliance/nutty_plugin/sail_cSim\n")

    # fix the test bench by providing the correct path of the rom image
soc_tb = os.path.join(get_repo_path(),"test/rv_compliance/soc_verilog_tb.v")
existing_patch = []
with open(soc_tb,'r') as f:
    existing_patch = f.readlines()
with open(soc_tb,'a+') as f:
    if not any(["//tb_updated" in line for line in existing_patch]):
        image_rom = os.path.join(get_repo_path(),"test/riscof_work/image.rom")
        f.writelines("//tb_updated\n")
        f.writelines(f"initial begin\n")
        f.writelines(f'$readmemh("{image_rom}", top.U$$0.imem._mem);\n')
        f.writelines(f"end\n")
        f.writelines(f"endmodule\n")
os.system(f"riscof run --config={config_ini} --suite={test_suite} --env={test_env} --work-dir={work_dir} --no-browser")