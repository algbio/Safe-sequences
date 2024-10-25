from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import argparse
import re

def parse_input_file(filename):
    data = defaultdict(list)
    current_graph = None
    total_graphs = 0

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()

            if line.startswith('#Graph'):
                current_graph = int(line.split()[1])
                #total_graphs += 1

            elif current_graph is not None:
                if re.match(r'\d+,\s*\d+,\s*\d+', line):
                    # Parse n, m, w
                    n, m, w = map(int, line.split(','))
                    data[current_graph] = {
                        'n': n, 'm': m, 'w': w,
                        'solved default': None, 'total time default': None,
                        'solved paths heur': None, 'total time paths heur': None,
                        'solved sequences heur': None, 'total time sequences heur': None,
                        'preprocess paths heur': None, 'preprocess sequences heur': None,
                    }
                
                    if w>=30: #hack!
                        total_graphs += 1

                elif 'solved' in line or 'time' in line or 'preprocess' in line:
                    key, value = line.split(':')
                    key = key.strip()
                    value = value.strip()

                    if value in ['True', 'False']:
                        value = value == 'True'
                    else:
                        value = float(value)

                    if key in data[current_graph]:
                        data[current_graph][key] = value
            elif 'Timeout' in line:
                timeout = int(re.search(r'Timeout:(\d+)', line).group(1))
    return timeout,data,total_graphs


def plot_cumulative_runtime(timeout, data, total_graphs, filename):
    categories = {
        'No safety': 'total time default',
        'Safe paths': 'total time paths heur',
        'Safe sequences': 'total time sequences heur'
    }
    colors = {'No safety': 'red', 'Safe paths': 'blue', 'Safe sequences': 'purple'}
    
    # Initialize the plot
    plt.figure(figsize=(7, 6))

    data = list(data.values()) #list of dicts like [ {n:5, m:6, w:90, solved default: True,...}, ...]

    data = list ( filter( lambda x: x['w']>=30 , data)) #hack!

    for label, key in categories.items():
        runtimes = [entry[key] for entry in data if entry[key] is not None]
        runtimes = list(filter(lambda x : x!=0, runtimes))
        runtimes.sort()
        cumulative = np.arange(1, len(runtimes) + 1) / total_graphs * 100 # Compute the cumulative proportion of instances solved
        plt.plot(runtimes, cumulative, label=f'{label}', color=colors[label])

    plt.xlabel('Runtime (seconds)')
    plt.ylabel('Proportion of Instances Solved (\%)')
    plt.xlim(0, timeout) #max(timeout, max(runtimes))
    plt.ylim(40, 100)
    plt.legend(loc='lower right', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.savefig(filename+".plot.pdf")
    
    #plt.savefig("output1", facecolor='y', bbox_inches="tight", pad_inches=0.3, transparent=True) #Saving figure by changing parameter values



def main():

    parser = argparse.ArgumentParser(description='Process inputs.')

    parser.add_argument('-i', '--input'  , required=True, help='Input file path')

    args = parser.parse_args()

    filename                      = args.input
    timeout,parsed_data,graph_num = parse_input_file(filename)

    plot_cumulative_runtime(timeout,parsed_data,graph_num,filename)



if __name__ == "__main__":
    main()
