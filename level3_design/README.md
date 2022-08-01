# Level-2 Design Verification

The verification environment was setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![Setup Screenshot](https://user-images.githubusercontent.com/42858487/180610171-078c23ad-e0ba-476a-814d-15ee0c7eec8e.PNG)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test was developed as explained. The test drives inputs to the mips_16_core_top.v (dut). The only inputs to the dut are clock (dut.clk) and reset(dut.rst). The reset signal ``dut.rst`` is an active high signal.

## Test : Testing the in-built assembly level program with the mips processor

The test program instructions were already loaded into the instruction_memory using an assembler.


## Test Scenario **(Important)**
- Test Inputs: The cocotb testbench was only used to provide the clock signal and reset signal.
- Expected Output: The expected output for each instruction can be seen on the terminal window along with the PC value.  
- Observed Output: All of the instructions were seen and also the branching was happening in the output.

## Successful Integration of my chosen design into Vyoma's UpTickPro Platform

![Passed test cases](https://user-images.githubusercontent.com/42858487/182201422-82b2b8e4-0aa3-4cc7-8334-b0de455f85cb.PNG)


## The Assembly Program loaded in the instruction memory

![assembly program](https://user-images.githubusercontent.com/42858487/182201475-ecd76985-5548-4b1c-9a02-b8d59df11689.PNG)

## Cocotb Test Developed For my Design

![cococtb test](https://user-images.githubusercontent.com/42858487/182201514-a841416a-7551-4cb8-9937-a50fba8a8f9c.PNG)

## Failed Test Cases

I could not perfectly understand how the instructions were being loaded from the synthesized ``rom`` into the ``dut``.

Although, I completely understood the design as I had submitted the initial report on the design. The design used five stage pipelining architecture. The pipeline structures are:
1. Instruction Fetch
2. Instruction Decode
3. Execute Stage
4. Memory Stage
5. Write Back Stage

## Design Bug

I did not insert a design bug as I had no clear stratergy on how to fail the test cases since I could not understand how to change the assembly level program.

## Design Fix

--NA--

## Verification Strategy

--NA--


## Is the verification complete ?

:'( No.
