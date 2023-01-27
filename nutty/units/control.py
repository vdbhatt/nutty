from amaranth import Elaboratable, Module, Signal, Cat, Const

from nutty.units.constants import Instr as I
from nutty.units.constants import MemOP as M


class ControlUnit(Elaboratable):
    def __init__(self):
        self.decoded_instr_i = Signal(6)
        self.rd_write_en_o = Signal()
        self.alu_op1_select_o = Signal()
        self.alu_op2_select_o = Signal()
        self.alu_op_select_o = Signal(5)
        self.mem_op_select_o = Signal(8)
        self.reg_write_src_ctl = Signal(2)

        self.do_jump_o = Signal()

    def elaborate(self, platform):
        m = Module()
        # rd_write_en_o
        with m.Switch(self.decoded_instr_i):
            with m.Case(
                I.LUI,
                I.AUIPC,
                I.JALR,
                I.JAL,
                I.LB,
                I.LH,
                I.LW,
                I.LBU,
                I.LHU,
                I.ADDI,
                I.SLTI,
                I.SLTIU,
                I.XORI,
                I.ORI,
                I.ANDI,
                I.SLLI,
                I.SRLI,
                I.SRAI,
                I.ADD,
                I.SUB,
                I.SLL,
                I.SLT,
                I.SLTU,
                I.XOR,
                I.SRL,
                I.SRA,
                I.OR,
                I.AND,
                I.CSRRW, I.CSRRS, I.CSRRC, I.CSRRWI, I.CSRRSI, I.CSRRCI,
                I.FENCE,
            ):
                m.d.comb += self.rd_write_en_o.eq(1)
            with m.Default():
                m.d.comb += self.rd_write_en_o.eq(0)
        # alu_op1_select_o
        with m.Switch(self.decoded_instr_i):
            with m.Case(I.AUIPC, I.JAL, I.BEQ, I.BNE, I.BLT, I.BGE, I.BLTU, I.BGEU):
                m.d.comb += self.alu_op1_select_o.eq(1)
            with m.Default():
                m.d.comb += self.alu_op1_select_o.eq(0)
        # alu_op2_select_o
        with m.Switch(self.decoded_instr_i):
            with m.Case(
                I.LUI,
                I.AUIPC,
                I.ADDI,
                I.SLTI,
                I.SLTIU,
                I.XORI,
                I.ORI,
                I.ANDI,
                I.SLLI,
                I.SRLI,
                I.SRAI,
                I.LB,
                I.LH,
                I.LW,
                I.LBU,
                I.LHU,
                I.SB,
                I.SH,
                I.SW,
                I.BEQ,
                I.BNE,
                I.BLT,
                I.BGE,
                I.BLTU,
                I.BGEU,
                I.JAL,
                I.JALR,
            ):
                m.d.comb += self.alu_op2_select_o.eq(1)
            with m.Case(
                I.ADD, I.SUB, I.SLL, I.SLT, I.SLTU, I.XOR, I.SRL, I.SRA, I.OR, I.AND
            ):
                m.d.comb += self.alu_op2_select_o.eq(0)
            with m.Default():
                m.d.comb += self.alu_op2_select_o.eq(0)
        # alu_op_select_o
        with m.Switch(self.decoded_instr_i):
            with m.Case(
                I.LB,
                I.LH,
                I.LW,
                I.LBU,
                I.LHU,
                I.SB,
                I.SH,
                I.SW,
                I.JAL,
                I.JALR,
                I.AUIPC,
                I.ADD,
                I.ADDI,
                I.BEQ,
                I.BNE,
                I.BLT,
                I.BGE,
                I.BLTU,
                I.BGEU,
            ):
                m.d.comb += self.alu_op_select_o.eq(1)
            with m.Case(I.LUI):
                m.d.comb += self.alu_op_select_o.eq(2)
            with m.Case(I.SUB):
                m.d.comb += self.alu_op_select_o.eq(3)
            with m.Case(I.SLT, I.SLTI):
                m.d.comb += self.alu_op_select_o.eq(4)
            with m.Case(I.SLTU, I.SLTIU):
                m.d.comb += self.alu_op_select_o.eq(5)
            with m.Case(I.XOR, I.XORI):
                m.d.comb += self.alu_op_select_o.eq(6)
            with m.Case(I.OR, I.ORI):
                m.d.comb += self.alu_op_select_o.eq(7)
            with m.Case(I.AND, I.ANDI):
                m.d.comb += self.alu_op_select_o.eq(8)
            with m.Case(I.SLL, I.SLLI):
                m.d.comb += self.alu_op_select_o.eq(9)
            with m.Case(I.SRL, I.SRLI):
                m.d.comb += self.alu_op_select_o.eq(10)
            with m.Case(I.SRA, I.SRAI):
                m.d.comb += self.alu_op_select_o.eq(11)
            with m.Default():
                m.d.comb += self.alu_op_select_o.eq(0)

        # mem_op_select_o
        with m.Switch(self.decoded_instr_i):
            with m.Case(I.LB):
                m.d.comb += self.mem_op_select_o.eq(M.LB)
            with m.Case(I.LH):
                m.d.comb += self.mem_op_select_o.eq(M.LH)
            with m.Case(I.LW):
                m.d.comb += self.mem_op_select_o.eq(M.LW)
            with m.Case(I.LBU):
                m.d.comb += self.mem_op_select_o.eq(M.LBU)
            with m.Case(I.LHU):
                m.d.comb += self.mem_op_select_o.eq(M.LHU)
            with m.Case(I.SB):
                m.d.comb += self.mem_op_select_o.eq(M.SB)
            with m.Case(I.SH):
                m.d.comb += self.mem_op_select_o.eq(M.SH)
            with m.Case(I.SW):
                m.d.comb += self.mem_op_select_o.eq(M.SW)
            with m.Default():
                m.d.comb += self.mem_op_select_o.eq(0)

        # reg_write_src_ctl
        with m.Switch(self.decoded_instr_i):
            with m.Case(I.LB, I.LH, I.LW, I.LBU, I.LHU):
                m.d.comb += self.reg_write_src_ctl.eq(0)
            with m.Case(I.JAL, I.JALR):
                m.d.comb += self.reg_write_src_ctl.eq(2)
            with m.Case(I.CSRRW, I.CSRRS, I.CSRRC, I.CSRRWI, I.CSRRSI, I.CSRRCI):
                m.d.comb += self.reg_write_src_ctl.eq(3)
            with m.Default():
                m.d.comb += self.reg_write_src_ctl.eq(1)
        # do_jump_o
        with m.Switch(self.decoded_instr_i):
            with m.Case(I.JAL, I.JALR):
                m.d.comb += self.do_jump_o.eq(1)
            with m.Default():
                m.d.comb += self.do_jump_o.eq(0)

        # # csr_wr_en_o
        # with m.Switch(self.decoded_instr_i):
        #     with m.Case(I.CSRRW, I.CSRRS, I.CSRRC, I.CSRRWI, I.CSRRSI, I.CSRRCI):
        #         m.d.comb += csr_wr_en_o.eq(1)
        #     with m.Default():
        #         m.d.comb += csr_wr_en_o.eq(1)

        # # csr_wr_data_o
        # with m.Switch(self.decoded_instr_i):
        #     with m.Case(I.CSRRW):
        #         m.d.comb += csr_wr_data_o.eq(1)
        #     with m.Case(I.CSRRS):
        #         m.d.comb += csr_wr_data_o.eq(2)
        #     with m.Case(I.CSRRC):
        #         m.d.comb += csr_wr_data_o.eq(3)
        #     with m.Case(I.CSRRWI):
        #         m.d.comb += csr_wr_data_o.eq(4)
        #     with m.Case(I.CSRRSI):
        #         m.d.comb += csr_wr_data_o.eq(5)
        #     with m.Case(I.CSRRCI):
        #         m.d.comb += csr_wr_data_o.eq(6)
        #     with m.Default():
        #         m.d.comb += csr_wr_data_o.eq(0)
        return m
