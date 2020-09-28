import numpy as np
import pandas as pd
import random
import os

EPSILON = 0.9
GAMMA = 0.85
ALPHA = 0.1
ACTIONS = ['wait', 'deliver']

class package:
    def __init__(self, clock, road_length):
        self.create_time = clock
        self.house_num = random.randint(1, road_length)


def package_generator(generate_prob, generate_flag):
    if random.random() < generate_prob:
        generate_prob = min(generate_prob + 0.02, 0.25)
        generate_flag = True
    else:
        generate_prob = max(generate_prob - 0.02, 0.05)
        generate_flag = False

    return generate_prob, generate_flag
    

# rewards for delivery
def deliver_rewards(loaded_package, clock, road_length, deliv_penalty):
    reward = deliv_penalty + 30 * road_length * len(loaded_package)
    for item in loaded_package:
        reward -= (((clock - item.create_time + 1) + (clock - item.create_time + \
            item.house_num)) * item.house_num / 2)
    return reward


# penalty for packages in the warehouse
def warehouse_penalty(warehouse, clock):
    penalty = 0
    for item in warehouse:
        penalty -= (clock - item.create_time)
    return penalty


def choose_action(state, q_table):
    state_actions = q_table.iloc[state, :]
    if (np.random.uniform() > EPSILON) or ((state_actions == 0).all()):
        action_name = np.random.choice(ACTIONS)
    else:
        action_name = state_actions.idxmax() 
    return action_name


def retrive_state(warehouse, road_length, truck_capacity):
    if not warehouse:
        state = 0
    else:
        state = (min(len(warehouse), truck_capacity + 1) - 1) * road_length \
            + max(item.house_num for item in warehouse)
    return state

def evaluation(q_table, road_length, truck_capacity, deliv_penalty, time=1000):
    gen_prob = 0.15
    gen_flag = False
    eval_clock = 1
    total_reward = 0
    warehouse = []
    loaded_package = []

    while (eval_clock < time):
        gen_prob, gen_flag = package_generator(gen_prob, gen_flag)
        if gen_flag == True:
            warehouse.append(package(eval_clock, road_length))

        state = retrive_state(warehouse, road_length, truck_capacity)
        action = q_table.iloc[state, :].idxmax()

        if action == 'wait':
            reward = warehouse_penalty(warehouse, eval_clock)
            # get next timestamp's status:
            eval_clock += 1
            gen_prob, gen_flag = package_generator(gen_prob, gen_flag)
            if gen_flag == True:
                warehouse.append(package(eval_clock, road_length))
        
        else: # action == 'deliver'
            for _ in range(truck_capacity):
                if not warehouse: break
                loaded_package.append(warehouse.pop(0)) # load packages
            deliv_reward = deliver_rewards(loaded_package, eval_clock, road_length, deliv_penalty)
            loaded_package = []

            penalty = 0
            if warehouse: # if warehouse is not empty
                # get the status when returning to the warehouse:
                for _ in range(max(item.house_num for item in warehouse)*2):
                    eval_clock += 1
                    gen_prob, gen_flag = package_generator(gen_prob, gen_flag)
                    if gen_flag == True:
                        warehouse.append(package(eval_clock, road_length))
                    penalty += warehouse_penalty(warehouse, eval_clock)
            reward = deliv_reward + penalty
                
        total_reward += reward

    print('Total reward is %d after %d timesteps, i.e. %.2f per step.' % \
        (total_reward, eval_clock, total_reward/eval_clock))



def main():
    road_length = int(input("road length"))
    truck_capacity = int(input("capacity"))
    deliv_penalty = int(input("penalty for start on deliever"))
    ticks = int(input("clock ticks"))
  
    q_table = pd.DataFrame(
        np.zeros(((truck_capacity + 1) * road_length + 1, len(ACTIONS))),
        columns=ACTIONS)
    # q_table = pd.DataFrame(
    #     np.random.random_sample(((truck_capacity + 1) * road_length + 1, len(ACTIONS))),
    #     columns=ACTIONS)

    # define state number as: (num of package in warehouse - 1) * road_length + 
    #                     furthest house to be delivered

    for _ in range(200):
        gen_prob = 0.15
        gen_flag = False
        clock = 1
        warehouse = []
        loaded_package = []
        # for _ in range(random.randint(0, road_length*truck_capacity)):
        #     gen_prob, gen_flag = package_generator(gen_prob, gen_flag)
        #     if gen_flag == True:
        #         warehouse.append(package(clock, road_length))
        #     clock += 1
        
        for _ in range(ticks):
            gen_prob, gen_flag = package_generator(gen_prob, gen_flag)
            if gen_flag == True:
                warehouse.append(package(clock, road_length))

            state = retrive_state(warehouse, road_length, truck_capacity) 
            action = choose_action(state, q_table)

            if action == 'wait':
                reward = warehouse_penalty(warehouse, clock)
                # get next timestamp's status:
                clock += 1
                gen_prob, gen_flag = package_generator(gen_prob, gen_flag)
                if gen_flag == True:
                    warehouse.append(package(clock, road_length))
            
            else: # action == 'deliver'
                for _ in range(truck_capacity):
                    if not warehouse: break
                    loaded_package.append(warehouse.pop(0)) # load packages
                deliv_reward = deliver_rewards(loaded_package, clock, road_length, deliv_penalty)
                loaded_package = []

                penalty = 0
                if warehouse: # if warehouse is not empty
                    # get the status when returning to the warehouse:
                    for _ in range(max(item.house_num for item in warehouse)*2):
                        clock += 1
                        gen_prob, gen_flag = package_generator(gen_prob, gen_flag)
                        if gen_flag == True:
                            warehouse.append(package(clock, road_length))
                        penalty += warehouse_penalty(warehouse, clock)
                reward = deliv_reward + penalty
                    
            next_state = retrive_state(warehouse, road_length, truck_capacity)

            q_predict = q_table.loc[state, action]
            q_target = reward + GAMMA * q_table.iloc[next_state, :].max()
            q_table.loc[state, action] += ALPHA * (q_target - q_predict)

    q_table.to_csv(os.path.expanduser('~/Desktop/dataframe.csv'), header=True)

    evaluation(q_table, road_length, truck_capacity, deliv_penalty)

if __name__ == '__main__':
    main()
