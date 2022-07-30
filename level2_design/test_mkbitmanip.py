# See LICENSE.iitm for details
# See LICENSE.vyoma for details
 
import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock
 
from model_mkbitmanip import *
 
# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1)
        signal.value <= 1
        yield Timer(1)
 
# Sample Test
@cocotb.test()
def run_test(dut):
 
    # clock
    cocotb.fork(clock_gen(dut.CLK))
 
    # reset
    dut.RST_N.value <= 0
    yield Timer(10)
    dut.RST_N.value <= 1
 
    ######### CTB : Modify the test to expose the bug #############
 
    err_count = 0
    for i in range (1000):
        # input transaction
        mav_putvalue_src1 = random.getrandbits(32)
        mav_putvalue_src2 = random.getrandbits(32)
        mav_putvalue_src3 = random.getrandbits(32)
 
        # intelligently choosing a random instruction
        mav_putvalue_instr = random.getrandbits(32)
        le = bin(mav_putvalue_instr)[2:].zfill(32)
 
        opcode_seq = [bin(51)[2:].zfill(7),bin(19)[2:].zfill(7)]
        func7_seq = [bin(32)[2:].zfill(7),bin(16)[2:].zfill(7),bin(48)[2:].zfill(7),bin(36)[2:].zfill(7),bin(20)[2:].zfill(7),bin(52)[2:].zfill(7),bin(5)[2:].zfill(7),bin(4)[2:].zfill(7)]
        func3_r_seq = [bin(1)[2:].zfill(3),bin(2)[2:].zfill(3),bin(3)[2:].zfill(3),bin(4)[2:].zfill(3),bin(5)[2:].zfill(3),bin(6)[2:].zfill(3),bin(7)[2:].zfill(3)]
        func3_imm_seq = ["001","101"]
        func7_imm_seq = [bin(4)[2:].zfill(5),bin(12)[2:].zfill(5),bin(9)[2:].zfill(5),bin(5)[2:].zfill(5),bin(13)[2:].zfill(5)]
        func7_2bit_seq = ["11","10","00"]
        #imm_value_1_seq = [bin(0)[2:].zfill(5),bin(1)[2:].zfill(5),bin(2)[2:].zfill(5),bin(4)[2:].zfill(5),bin(5)[2:].zfill(5),bin(16)[2:].zfill(5),bin(17)[2:].zfill(5),bin(18)[2:].zfill(5),bin(24)[2:].zfill(5),bin(25)[2:].zfill(5),bin(26)[2:].zfill(5)]
 
        # choosing the random sequences
        opcode = random.choices(opcode_seq,cum_weights = [35, 58],k=1)[0]
        func7 = random.choice(func7_seq)
        func3_r = random.choice(func3_r_seq)
        func3_imm = random.choice(func3_imm_seq)
        func7_imm = random.choice(func7_imm_seq)
        func7_2bit = random.choice(func7_2bit_seq)
        func7_fsri_1bit = random.choice(["0","1"])
 
        if (opcode == "0110011"): # R-type Instruction
            if(func7_2bit == "00"): # Normal R-type Instruction
                le = func7 + le[7:17] + func3_r + le[20:25] + opcode
            else: #R4-type Instruction
                le = le[0:5] + func7_2bit + le[7:17] + func3_imm + le[20:25] + opcode
 
        if (opcode == "0010011"): # I-type Instruction
            if(func7_fsri_1bit == "1"): # FSRI Instruction
                le = le[0:5] + func7_fsri_1bit + le[6:17] + "101" + le[20:25] + opcode
            else: # Normal I-type Instruction
                le = func7_imm + "0" + le[6:17] + func3_imm + le[20:25] + opcode
 
        mav_putvalue_instr = int(le,2)
 
        # expected output from the model
        expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)
 
        # driving the input transaction
        dut.mav_putvalue_src1.value = mav_putvalue_src1
        dut.mav_putvalue_src2.value = mav_putvalue_src2
        dut.mav_putvalue_src3.value = mav_putvalue_src3
        dut.EN_mav_putvalue.value = 1
        dut.mav_putvalue_instr.value = mav_putvalue_instr
   
        yield Timer(1)
 
        # obtaining the output
        dut_output = dut.mav_putvalue.value
 
        cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
        cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
       
        # comparison
        error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
        if (dut_output != expected_mav_putvalue):
            if (hex(expected_mav_putvalue) != "0x0"):
                err_count = err_count + 1
                cocotb.log.info(f'SRC1 = {hex(dut.mav_putvalue_src1.value)} \t SRC2 = {hex(dut.mav_putvalue_src2.value)}')
 
                result_andn = int(dut.mav_putvalue_src1.value) & ~int(dut.mav_putvalue_src2.value)
                result_andn = result_andn & 0xffffffff
                result_andn = (result_andn << 1) | 1
 
                result_and = int(dut.mav_putvalue_src1.value) & int(dut.mav_putvalue_src2.value)
                result_and = result_and & 0xffffffff
                result_and = (result_and << 1) | 1
                cocotb.log.info(f'ANDN = {hex(result_andn)} \t AND = {hex(result_and)}')              
                dut._log.info(error_message)
 
    final_error_message = f'The behaviour of the DUT differs from that of the model. The DUT fails for {err_count}/{i+1} instructions.'
    assert err_count == 0, final_error_message