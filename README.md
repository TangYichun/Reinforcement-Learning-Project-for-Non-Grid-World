# Intelligent robotic truck driver
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

### the state function explanation
I choose to set the state function as state=(#of package-1)*length of road+the furthest household requires delivery;
Since the length of road is one of the inputs from the user, number of the packages and the household is generated in the simulation. Hence, we can use the state to make the learning policy.
For example, if we have the road length = 20 (other inputs: capacity = 10, penalty for starting the delivery = -500, and clock ticks = 500), we will get a table of the states. 


![image](https://user-images.githubusercontent.com/41353447/121787780-333b7680-cb96-11eb-9f82-37e5315175c5.png)

Hence if we would like to know, for example, if we have packages labeled household #2, and #5, we would consider the state = (2-1)*20 + 5 = 25, hence we check the list, we can see here since wait = -0.2, deliver = 136.14, hence in this state, the learning policy suggest the agent should delivery the package instead of waiting.
I choose this way to represent the state because since it is 1-dimension, it is easy for the simulation step instead of considering 3 different states at the same time (the place, # of packages and the household that need the delivery service). For every grid in the table, the value is the q-value of the action it could take for that state. The agent could make the decision according to the q-value. (take the argmax(q-value)).



