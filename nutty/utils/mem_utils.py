import os
from pathlib import Path

def read_memory_file(file_path=None):
    instr_int = []
    if file_path :
        with open(file_path, "r") as f:
            instrs = f.readlines()
            for i in instrs:
                x = int(i, 16)
                instr_int.append(x)
        return instr_int
    else:
        return []
def get_repo_path():
    current_path = os.path.abspath(__file__)
    repo = Path(current_path).parent.parent.parent
    return repo

def get_dmem_size():
    return 0x2000

def get_imem_size():
    return 0x2000
