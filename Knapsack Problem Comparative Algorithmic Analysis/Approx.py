import os
import time
import argparse


class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

def read_knapsack_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    num_items, max_weight = map(int, lines[0].split())
    items = [Item(float(line.split()[0]), float(line.split()[1])) for line in lines[1:]]
    return max_weight, items

def knapsack_approximation(items, capacity):
    items_sorted = sorted(items, key=lambda x: x.value / x.weight, reverse=True)
    total_value = 0
    total_weight = 0
    selected_items = []
    solution_binary = [0] * len(items)

    for i, item in enumerate(items_sorted):
        if total_weight + item.weight <= capacity:
            selected_items.append(item)
            total_value += item.value
            total_weight += item.weight
            solution_binary[items.index(item)] = 1  # mark item as selected

    return total_value, selected_items, solution_binary


def write_output_files(fileName, cutoff, seed, total_value, solution_binary, start_time):
    instanceName = os.path.basename(fileName)
    instanceDir = os.path.dirname(fileName)

    resDir = os.path.join(instanceDir,instanceName+"_Approx")
    # Create directories if they do not exist
    os.makedirs(resDir, exist_ok=True)

    # Define file names
    sol_basename = f"{instanceName}"+"_Approx_"+f"{cutoff}_{seed}.sol"
    trace_basename = f"{instanceName}"+"_Approx_"+f"{cutoff}_{seed}.trace"
    sol_filename = os.path.join(resDir,sol_basename)
    trace_filename = os.path.join(resDir,trace_basename)

    # Write solution file
    with open(sol_filename, 'w') as f:
        f.write(f"{int(total_value)}\n")
        f.write(','.join(str(i) for i, chosen in enumerate(solution_binary) if chosen))

    # Write trace file
    with open(trace_filename, 'w') as f:
        elapsed_time = time.time() - start_time
        f.write(f"{elapsed_time:.2f}, {int(total_value)}\n")


def Approx(fileName,cutoff,seed):
    capacity, items = read_knapsack_data(fileName)
    start_time = time.time()
    total_value, selected_items, solution_binary = knapsack_approximation(items, capacity)
    write_output_files(fileName,  cutoff, seed, total_value, solution_binary, start_time)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Knapsack Approximation Algorithm")
    parser.add_argument('-inst', type=str, required=True, help='Dataset filename')
    parser.add_argument('-alg', type=str, required=True, help='Algorithm to use')
    parser.add_argument('-time', type=int, required=True, help='Cutoff time in seconds')
    parser.add_argument('-seed', type=int, required=True, help='Random seed')
    args = parser.parse_args()
    Approx(args.inst,args.time,args.seed)
