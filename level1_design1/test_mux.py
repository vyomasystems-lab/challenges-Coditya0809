# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mux_duplicate_select(dut):
    """Test for mux2"""

    cocotb.log.info('##### CTB: Develop your test here ########')

    seeded_rand_value = random.randint(0,3)

    # input driving
    dut.inp11.value = (1 + seeded_rand_value) % 4
    # giving dut.inp12 a non-zero value not equal to inp11 to detect error always
    dut.inp12.value = seeded_rand_value + 2 if (0 == seeded_rand_value) else seeded_rand_value
    dut.sel.value = 12

    await Timer(2, units='ns')

    assert dut.out.value == dut.inp12.value, f"Mux output is incorrect: Expected Output != Model Output : {dut.inp12.value} != {dut.out.value}. Expected Value: {dut.inp12.value}"

@cocotb.test()
async def test_mux_last_input(dut):
    """Test for mux2"""
    # input driving
    dut.inp30.value = 3
    dut.sel.value = 30

    await Timer(2, units='ns')

    assert dut.out.value == dut.inp30.value, f"Mux output is incorrect: Expected Output != Model Output : {dut.inp30.value} != {dut.out.value}. Expected Value: {dut.inp30.value}"