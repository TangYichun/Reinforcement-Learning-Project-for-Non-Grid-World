# robotic truck project
Yichun Tang

### Instruction for compiling:
\
The program will ask the user to provide input for:

1. Road length: any positive number
2. Capacity: any positive number
3. Penalty for starting on delivering: any negative number
4. Clock-tick: any positive number

Please provide the number accordingly as it request.

### Result Illustration:

The output contains a csv file for the table of the learning policy, which should be generated in the same directory as the code located. For every grid in the table, the value is the q-value of the action it could take for that state. The agent could make the decision according to the q-value. (take the argmax(q-value)). Also, in the console, it will provide the output for the total reward and the average reward.

State: (num of package in warehouse - 1) * road_length + furthest house to be delivered
Information requires for interpreting the policy: the number of package in the warehouse, the length of road, and the furthest household that request delivering the parcel(s). For the detailed explanation of the state, please check the explanation in the write-up file.
