# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""

    cocotb.log.info('##### CTB: Develop your test here ########')

    # input driving
    seeded_rand_value = random.randint(0,3)
    dut.inp11.value = (1 + seeded_rand_value) % 4
    # giving dut.inp12 a non-zero value not equal to inp11 to detect error always
    dut.inp12.value = seeded_rand_value + 2 if (0 == seeded_rand_value) else seeded_rand_value
    dut.sel.value = 12
    await Timer(2, units='ns')
    assert dut.out.value == dut.inp12.value, f"Mux output is incorrect: Expected Output != Model Output : {dut.inp12.value} != {dut.out.value}. Expected Value: {dut.inp12.value}"