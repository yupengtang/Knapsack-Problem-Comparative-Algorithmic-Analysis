import random
import time
import numpy as np
import os

class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

#Calculate the value of the solution
def value_sum(sol, items):
    return sum(item.value for item, chosen in zip(items, sol) if chosen)

#sum up all the weight to check whether it exceeds the limit or not
def weight_sum(sol, items):
    return sum(item.weight for item, chosen in zip(items, sol) if chosen)

def hill_climbing(items, max_weight,random_seed):
    #  initialize a binary solution
    start_time = time.time()
    time_list = []


    n = len(items)
    r = list(range(n))
    random.shuffle(r)

    # current_solution_binary = [0] * n
    # random.seed(random_seed)

    np.random.seed(random_seed)
    all_chosen = [1] * n
    avg_weight =  weight_sum(all_chosen, items)/n
    initProb = max_weight / avg_weight/100
    # print(initProb)
    current_solution_binary = [0]*n
    # current_solution_binary = np.random.binomial(1, initProb, size=n)
    #
    # while weight_sum(current_solution_binary,items) > max_weight:
    #     current_solution_binary = np.random.binomial(1, initProb, size=n)

    # Ensure the initial solution is within the weight limit
    # print('initial solution:', current_solution_binary)
    current_value = value_sum(current_solution_binary, items)
    value_list = [current_value]
    time_list.append((time.time() - start_time)*1000)
    # Iterate to check whether the solution is improved
    incremented = True
    while incremented:# and (time.time() - start_time) < cutoff:
        incremented = False
        for i in r:
            neighbor = current_solution_binary.copy()
            # Flip the bit to generate a neighbor
            if neighbor[i] == 1:
                neighbor[i] = 0
            else:
                neighbor[i] = 1
            #find the first neighbor that provides a bigger solution than the current one
            if weight_sum(neighbor, items) <= max_weight:
                neighbor_value = value_sum(neighbor, items)
                if neighbor_value > current_value:
                    current_solution_binary = neighbor
                    # print('new binary list: ',current_solution_binary)
                    current_value = neighbor_value
                    value_list.append(current_value)
                    # print("--- %s seconds ---" % (time.time() - start_time))

                    incremented = True
                    time_list.append((time.time() - start_time))
                    break  # Move to the next iteration after finding an improvement
    final_solution = [items[i] for i, chosen in enumerate(current_solution_binary) if chosen]
    return final_solution, current_solution_binary, time_list, value_list


def HCOnce(fileName,cutoff,seed):
    with open(fileName, 'r') as file:
        lines = file.readlines()
    first_line = lines[0].strip().split()
    num_items, knapsack_capacity = int(first_line[0]), int(first_line[1])
    items_from_file = [Item(float(line.split()[0]), float(line.split()[1])) for line in lines[1:]]
    #final_result_binary = [0] * len(items_from_file)
    best_solution, result_binary, time, value = hill_climbing(items_from_file, knapsack_capacity,seed)
    final_value = value[-1]

    instanceName = os.path.basename(fileName)
    instanceDir = os.path.dirname(fileName)
    filename = instanceName +"_HC_"+str(cutoff)+"_"+str(seed)
    resDir = os.path.join(instanceDir,instanceName+"_HC")
    if not os.path.exists(resDir):
        os.makedirs(resDir)
    solFile = os.path.join(resDir,filename+".sol")
    traceFile = os.path.join(resDir,filename+".trace")

    f = open(solFile,"w")
    f.write(str(final_value)+ '\n')
    to_write = ''
    for m in range(len(result_binary)):
        if result_binary[m] == 1:
            to_write += str(m) + ','
    to_write = to_write[:-1]
    f.write(to_write)
    f.close()

    ftrace = open(traceFile, "w")
    for m in range(len(value)):
        ftrace.write(str(time[m]))
        ftrace.write(',')
        ftrace.write(str(value[m]) + '\n')
    ftrace.close()


if __name__ == "__main__":
    # Define items and capacity
    cutoff = 1000
    def generate_file(a, cutoff, seed, type):

        # seed = 100
        # file_path = 'DATASET/test/KP_s_0'+a
        file_path = 'DATASET/'+type + '_scale/'+type+'_'+a
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Process the first line to extract the number of items and the capacity of the knapsack
        first_line = lines[0].strip().split()
        num_items, knapsack_capacity = int(first_line[0]), int(first_line[1])
        # print(first_line)
        # print(num_items)
        # print(knapsack_capacity)
        # Process subsequent lines to extract the value and weight of each item
        items_from_file = [Item(float(line.split()[0]), float(line.split()[1])) for line in lines[1:]]
        final_result_binary = [0] * len(items_from_file)
        # print(items_from_file[0].value)


        # Run the hill climbing algorithm
        # for i in range (100):

        best_solution, result_binary, time, value = hill_climbing(items_from_file, knapsack_capacity,seed)
        final_value = value[-1]

        #Generate output solution file

        f = open('output/sol/'+ type + '_scale/' + a + '_LS1_'+ str(cutoff)+ '_'+str(seed) +'.sol', "w")
        f.write(str(final_value)+ '\n')
        to_write = ''
        for m in range(len(result_binary)):
            if result_binary[m] == 1:
                to_write += str(m) + ','
        to_write = to_write[:-1]
        f.write(to_write)
        f.close()

    #generate trace file

        f = open('output/trace_file/'+ type + '_scale/' + a + '_LS1_'+ str(cutoff)+ '_' +str(seed)+'.trace', "w")

        for m in range(len(value)):
            f.write(str(time[m]))
            f.write(',')
            f.write(str(value[m]) + '\n')
        f.close()

    for a in range(1, 11):
        for seed in range(1,11):
            print(a, seed)
            generate_file(str(a), cutoff, seed, 'small')
