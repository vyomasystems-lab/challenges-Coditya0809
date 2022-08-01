# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer

@cocotb.test()
async def test_mips_16(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.rst.value = 1
    await FallingEdge(dut.clk)  
    dut.rst.value = 0
    await FallingEdge(dut.clk)

    cocotb.log.info('#### CTB: Develop your test here! ######')

    for i in range (100):
        dut._log.info(f'PC: {dut.pc.value} \t INSTRUCTION: {dut.instruction.value}')
        dut._log.info(f'The Output of EX_stage after cycle {i+1} is: {dut.EX_pipeline_reg_out.value.binstr}')
        await FallingEdge(dut.clk)

    error_message = f'The desgin fails as the DUT value does not match the expected (model) value.'
    # assert some_condition_to_check, f'error_message'
