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
    for i in range (1):
        # input transaction
        mav_putvalue_src1 = random.randint(0,2**32-1)
        mav_putvalue_src2 = random.randint(0,2**32-1)
        mav_putvalue_src3 = random.randint(0,2**32-1)

        # intelligently choosing a random instruction
        mav_putvalue_instr = bin(0)[2:].zfill(32)
        opcode_seq = [bin(51)[2:].zfill(7),bin(19)[2:].zfill(7)]
        func7_seq = [bin(32)[2:].zfill(7),bin(16)[2:].zfill(7),bin(48)[2:].zfill(7),bin(36)[2:].zfill(7),bin(20)[2:].zfill(7),bin(52)[2:].zfill(7),bin(5)[2:].zfill(7),bin(4)[2:].zfill(7)]
        func3_seq = [bin(1)[2:].zfill(3),bin(2)[2:].zfill(3),bin(3)[2:].zfill(3),bin(4)[2:].zfill(3),bin(5)[2:].zfill(3),bin(6)[2:].zfill(3),bin(7)[2:].zfill(3)]
        func7_imm_seq = [bin(4)[2:].zfill(5),bin(12)[2:].zfill(5),bin(9)[2:].zfill(5),bin(5)[2:].zfill(5),bin(13)[2:].zfill(5)]
        func7_2bit_seq = ["11","10"]
        func7_1bit_seq = ["1","0"]
        func7_fsri_1bit_seq = ["0","1"]
        func7_imm_SHFL_seq = ["000010"]
        imm_value_seq = ["1","0"]
        imm_value_1_seq = [bin(0)[2:].zfill(5),bin(1)[2:].zfill(5),bin(2)[2:].zfill(5),bin(4)[2:].zfill(5),bin(5)[2:].zfill(5),bin(16)[2:].zfill(5),bin(17)[2:].zfill(5),bin(18)[2:].zfill(5),bin(24)[2:].zfill(5),bin(25)[2:].zfill(5),bin(26)[2:].zfill(5)]

        le = func7_seq[-3]+"1111111111"+func3_seq[4]+"11111"+opcode_seq[0]

        length = 32
        # le = bin(0)[2:].zfill(length)
        # le = bin(random.randint(0,2**32-1))[2:].zfill(32)
        opcode = le[-7::]
        func3 = le[length-15:length-12]
        func7 = le[length-32:length-25]
        func7_imm = le[length-32:length-27]
        func7_2bit = le[length-27:length-25]
        func7_1bit = le[length-28:length-27]
        func7_fsri_1bit = le[length-27:length-26]
        func7_imm_SHFL = le[length-32:length-26]
        imm_value = le[length-25:length-20]
        imm_value_1 = le[length-25:length-20]
        fsr_imm_value = le[length-26:length-20]

        dut._log.info(f'{le}')

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
            err_count = err_count + 1
            dut._log.info(error_message)

    final_error_message = f'The behaviour of the DUT differs from that of the model.'
    assert err_count == 0, final_error_message
