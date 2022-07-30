# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer

@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    cocotb.log.info('#### CTB: Develop your test here! ######')

    test_seq = [1,1,0,1,1]
    dut.inp_bit.value = test_seq[0]
    await FallingEdge(dut.clk)
    dut.inp_bit.value = test_seq[1]
    await FallingEdge(dut.clk)
    dut.inp_bit.value = test_seq[2]
    await FallingEdge(dut.clk)
    dut.inp_bit.value = test_seq[3]
    await FallingEdge(dut.clk)
    dut.inp_bit.value = test_seq[4]
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 0               # driving the inp_bit to 0 to allow another test case to execute, since this value is propagating to the next test and changing the current_state value
    await Timer(1, units='ns')

    assert dut.seq_seen.value == 1, f'Sequence must be detected but is not detected. Given sequence = {test_seq}. Model Output: {dut.seq_seen.value} Expected Ouput: 1'

@cocotb.test()
async def test_seq_bug2(dut):
    """Test for seq detection """
    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)
    dut.reset.value = 0
    await FallingEdge(dut.clk)

    cocotb.log.info('#### CTB: Develop your test here! ######')

    test_seq = [1,0,1,0,1,1]
    dut.inp_bit.value = test_seq[0]
    await FallingEdge(dut.clk)
    dut.inp_bit.value = test_seq[1]
    await FallingEdge(dut.clk)
    dut.inp_bit.value = test_seq[2]
    await FallingEdge(dut.clk)
    dut.inp_bit.value = test_seq[3]
    await FallingEdge(dut.clk)
    dut.inp_bit.value = test_seq[4]
    await FallingEdge(dut.clk)
    dut.inp_bit.value = test_seq[5]
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 0             # driving the inp_bit to 0 to allow another test case to execute, since this value is propagating to the next test and changing the current_state value
    await Timer(1, units='ns')

    assert dut.seq_seen.value == 1, f'Sequence must be detected but is not detected. Given sequence = {test_seq}. Model Output: {dut.seq_seen.value} Expected Ouput: 1'
