from amaranth import Mux
from amaranth.sim import Simulator
from amaranth import Elaboratable, Memory, Signal, Const, Cat, Module
from nutty.units.alu import ALU
from minerva.gpr import File as RegisterFile
from nutty.units.decoder import Decoder
from nutty.units.control import ControlUnit
from nutty.units.gen_immediate import GenImmediate
from nutty.units.branch import Branch
from nutty.units.lsu import LSU

class Nutty(Elaboratable):
    def __init__(self):
        # instr mem
        self.instr_mem_valid_i = Signal()
        self.instr_mem_ready_o = Signal()
        self.instr_mem_addr_o = Signal(32)
        self.instr_mem_data_i = Signal(32)

        # data mem
        self.data_mem_addr_o = Signal(32)

        self.data_mem_read_valid_i = Signal()
        self.data_mem_read_ready_o = Signal()
        self.data_mem_data_i = Signal(32)

        self.data_mem_write_valid_o = Signal()
        self.data_mem_write_ready_i = Signal()
        self.data_mem_data_o = Signal(32)
        self.data_mem_write_mask_o = Signal(4)

        self.pc = Signal(32)
        self.pc_plus_4 = Signal(32)

    def elaborate(self, platform):
        m = Module()
        alu_op1 = Signal(32)
        alu_op2 = Signal(32)
        pc_next = Signal(32)

        m.submodules.regs = regs = RegisterFile(width=32, depth=32)
        m.submodules.decoder = decoder = Decoder()
        m.submodules.imm = imm = GenImmediate()
        m.submodules.branch = branch = Branch()
        m.submodules.control_unit = control_unit = ControlUnit()
        m.submodules.lsu = lsu = LSU()
        m.submodules.alu = alu = ALU()

        # Decoder
        m.d.comb += regs.rp1.addr.eq(decoder.rs1_o)
        m.d.comb += regs.rp2.addr.eq(decoder.rs2_o)

        # imm
        # control
        m.d.comb += control_unit.decoded_instr_i.eq(decoder.opcode_o)

        # Mux works as c lang condition ? true branch : false branch
        m.d.comb += alu_op1.eq(Mux(control_unit.alu_op1_select_o,
                                   self.pc, regs.rp1.data))
        m.d.comb += alu_op2.eq(Mux(control_unit.alu_op2_select_o,
                                   imm.immediate_o, regs.rp2.data))
        # ALU
        m.d.comb += alu.op1_i.eq(alu_op1)
        m.d.comb += alu.op2_i.eq(alu_op2)
        m.d.comb += alu.control_i.eq(control_unit.alu_op_select_o)

        # BRANCH
        m.d.comb += branch.op1_i.eq(regs.rp1.data)
        m.d.comb += branch.op2_i.eq(regs.rp2.data)
        m.d.comb += branch.control_i.eq(decoder.branch_type_o)
        # LSU
        m.d.comb += lsu.addr_i.eq(alu.result_o)
        m.d.comb += lsu.lsu_op_i.eq(control_unit.mem_op_select_o)
        m.d.comb += lsu.data_i.eq(regs.rp2.data)
        m.d.comb += lsu.data_mem_read_data_i.eq(self.data_mem_data_i)
        m.d.comb += lsu.data_mem_read_valid_i.eq(self.data_mem_read_valid_i)
        m.d.comb += lsu.data_mem_write_ready_i.eq(self.data_mem_write_ready_i)
        m.d.comb += self.data_mem_addr_o.eq(lsu.data_mem_addr_o)
        m.d.comb += self.data_mem_read_ready_o.eq(lsu.data_mem_read_ready_o)
        m.d.comb += self.data_mem_data_o.eq(lsu.data_mem_write_data_o)
        m.d.comb += self.data_mem_write_mask_o.eq(lsu.data_mem_write_mask_o)
        m.d.comb += self.data_mem_write_valid_o.eq(lsu.data_mem_write_valid_o)

        # PC
        m.d.comb += pc_next.eq(Mux(((branch.branch_taken_o & decoder.branch_instr_o)
                               | control_unit.do_jump_o), alu.result_o, self.pc_plus_4))
        m.d.comb += self.pc_plus_4.eq(self.pc+4)
        m.d.comb += self.instr_mem_addr_o.eq(Cat(self.pc[2:],2*[0]))
        # assign reg address
        m.d.comb += regs.wp.addr.eq(decoder.rd_o)
        # FSM
        with m.FSM(reset="FETCH"):
            with m.State("FETCH"):
                m.d.sync += self.instr_mem_ready_o.eq(1)
                with m.If(self.instr_mem_valid_i):
                    m.d.sync += decoder.instr_i.eq(self.instr_mem_data_i)
                    m.d.sync += imm.instr_i.eq(self.instr_mem_data_i)
                    m.d.sync += self.instr_mem_ready_o.eq(0)
                    m.next = "DECODE"
            with m.State("DECODE"): # need to give time for reading regs
                with m.If(decoder.illegal_instr):
                    m.next = "ILLEGAL_INSTR"
                with m.Else():
                    m.next = "MEMORY"
            with m.State("EXECUTE"):
                m.next = "MEMORY"
            # make sure that no memory related signal change their value outside
            # memory state.
            # to ensure this let's have a signal which indicates that we are in memory state
            with m.State("MEMORY"):
                m.d.comb += lsu.in_memory_transaction.eq(1)
                with m.If(~lsu.mem_done_o & control_unit.mem_op_select_o.any()):
                    m.next = "MEMORY"
                with m.Else():
                    m.next = "WRITE_BACK"
            with m.State("WRITE_BACK"):
                with m.If(decoder.rd_o == 0):
                    m.d.comb += regs.wp.en.eq(0)
                with m.Else():
                    m.d.comb += regs.wp.en.eq(control_unit.rd_write_en_o)
                with m.Switch(control_unit.reg_write_src_ctl):
                    with m.Case(0):  # from memory it's load instr.
                        m.d.comb += regs.wp.data.eq(lsu.data_o)
                        # m.d.comb += regs.wp.en.eq(1)
                    with m.Case(1):
                        m.d.comb += regs.wp.data.eq(alu.result_o)
                        # m.d.comb += regs.wp.en.eq(1)
                    with m.Case(2):
                        m.d.comb += regs.wp.data.eq(self.pc_plus_4)
                        # m.d.comb += regs.wp.en.eq(1)
                    with m.Default():
                        m.d.comb += regs.wp.data.eq(0xdeadbeef)
                        m.d.comb += regs.wp.en.eq(0)  # no harm done
                m.d.sync += self.pc.eq(pc_next)
                m.next = "FETCH"
            with m.State("ILLEGAL_INSTR"):
                m.next = "ILLEGAL_INSTR"
        return m

if __name__ == "__main__":
    dut = Nutty()

    def test_process():
        while True:
            yield dut.pc.eq(0x0)
            yield

    sim = Simulator(dut)
    sim.add_clock(1/1e6)
    sim.add_sync_process(test_process)

    with sim.write_vcd("nutty.vcd"):
        sim.run_until(20e-6)
