# Level-1 Design-2 Verification

The verification environment was setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.


![](https://imgur.com/a/8xa4HqX.png)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test was developed as explained. The test drives inputs to the Design Under Test (1011 Sequence detector module here) which takes in 1-bit input *inp_bit* and gives 1-bit output *seq_seen* which goes high when an input sequence of 1011 is detected in an overlapping sense (Overlapping a non-sequence).

## Test 1 : Input 1<ins>1011</ins> not detected as a sequence

The values were assigned to the input port using 
```
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

```

The assert statement was used for comparing the mux's output to the expected value.

The following assert statement was used:
```
assert dut.seq_seen.value == 1, f'Sequence must be detected but is not detected. Given sequence = {test_seq}. Model Output: {dut.seq_seen.value} Expected Ouput: 1'
```
## Test Scenario 1 **(Important)**
- Test Inputs: An input test sequence 11011 was driven to the sequence detector
- Expected Output: seq_seen = 1 
- Observed Output in the DUT dut.seq_seen.value = 0

## Test 2 : Input 10<ins>1011</ins> not detected as a sequence

The values were assigned to the input port using 
```
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

```

The assert statement was used for comparing the mux's output to the expected value.

The following assert statement was used:
```
assert dut.seq_seen.value == 1, f'Sequence must be detected but is not detected. Given sequence = {test_seq}. Model Output: {dut.seq_seen.value} Expected Ouput: 1'
```

## Test Scenario 2 **(Important)**
- Test Inputs: An input test sequence 101011 was driven to the sequence detector
- Expected Output: seq_seen = 1 
- Observed Output in the DUT dut.seq_seen.value = 0

## Failed Test Cases

![](https://imgur.com/a/Moiofox.png)

Output mismatches for the above input sequence proving that there is a design bug

## Design Bug
Based on the above test inputs and analysing the design, we see the following

```
case(current_state)
    IDLE:
    begin
    if(inp_bit == 1)
        next_state = SEQ_1;
    else
        next_state = IDLE;
    end
    SEQ_1:
    begin
    if(inp_bit == 1)
        next_state = SEQ_1;
    else
        next_state = IDLE;      <==== BUG, must remain in SEQ_1
    end
    SEQ_10:
    begin
    if(inp_bit == 1)
        next_state = SEQ_101;
    else
        next_state = IDLE;
    end
    SEQ_101:
    begin
    if(inp_bit == 1)
        next_state = SEQ_1011;
    else
        next_state = IDLE;      <==== BUG, must change to SEQ_10
    end
    SEQ_1011:
    begin
    next_state = IDLE;
    end
    endcase
```
For the seq_detect_1011 design, the logic for case SEQ_1 when *inp_bit* is 1, changes state to *IDLE*. Therefore, when the sequence occurs after *odd number* of ones '1', the sequence, although occured, does not get detected.

Also, another bug in the logic is for the case SEQ_101 when *inp_bit* is 0, changes state to *IDLE*. Therefore, when the suquence occurs after the combination '10', it will not be detected.

The design was fixed by simply, reatining the state ``SEQ_1`` when inp_bit ``1`` occurs and for ``SEQ_101`` when inp_bit is ``0``, the state is limited to change to ``SEQ_10``, since a ``10`` has already been detected of the sequence ``1011``.

## Design Fix
Updating the design and re-running the test makes the test pass.

![](https://imgur.com/a/GbMQa1o.png)

The updated design is checked in as seq_detect_1011_fix.v

## Verification Strategy

The stratergy I followed to detect the bugs was simple. First, I drew a state transition diagram from the problem specifications. Then, I confirmed the state transitions by comparing my state transition diagram to the state transitions in the design file.

## Is the verification complete ?

I am not quite sure! Although the functionality of the design is as per the specifications, we can never be sure because of the huge amount of possibilities of the input bit sequences. However, I am very confident that any input sequence will be correctly detected if the ``current_state`` values don't get forced to change due to other hardware malfunctions.