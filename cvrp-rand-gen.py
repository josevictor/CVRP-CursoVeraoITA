import math
import random
import sys
import matplotlib.pyplot as plt

class RndGenCVRP:

    """Instance format for EUC2D:
    NAME : A-n32-k5
    COMMENT : (Augerat et al, No of trucks: 5, Optimal value: 784)
    TYPE : CVRP
    DIMENSION : 32
    EDGE_WEIGHT_TYPE : EUC_2D 
    CAPACITY : 100
    NODE_COORD_SECTION 
     1 82 76
     2 96 44
    1 35 35
    2 41 49
    ...
    32 98 5
    DEMAND_SECTION 
    1 0 
    2 19 
    3 21     
    ...
    31 14 
    32 9 
    DEPOT_SECTION 
    1  
    -1  
    EOF     
	"""
    
    def __init__(self):
        pass     
        
    def generate_uniform(self, file_name, instance_name, num_nodes, capacity, seed):
    
        # Initialize random seed
        random.seed(seed)
        
        X = []
        Y = []
            
        # Setting some bounds about capacity to generate only feasible solutions
        total_demand = 0
        node_demand = dict()
        for i in range(1,num_nodes+1):
            demand = random.randint(1, capacity)
            node_demand[i] = demand
            total_demand += demand
            
        print(f'Total demand: {total_demand}\n')
            
        # Estimate the number of vehicles needed to solve the problem
        num_vehicles = math.ceil(total_demand / capacity)
    
        # Creates an empty file to write instances from data
        output_file = open(file_name, 'w+')
        
        # Writes the file header, considering the input file is described as EUC_2D CVRP format
        output_file.write(f'NAME : {instance_name}\n') 
        output_file.write(f'COMMENT : Random generated instance, No. of vehicles {num_vehicles}, capacity {capacity}, Optimal value: Unknown\n') 
        output_file.write(f'TYPE : CVRP\n') 
        output_file.write(f'DIMENSION : {num_nodes}\n') 
        output_file.write(f'EDGE_WEIGHT_TYPE : EUC_2D\n') 
        output_file.write(f'CAPACITY : {capacity}\n')
        output_file.write(f'NODE_COORD_SECTION\n')
        
        for i in range(1,num_nodes+1):
            coord_x = random.uniform(0.0, 1.0)
            coord_y = random.uniform(0.0, 1.0)
        
            output_file.write(f'{i} {coord_x} {coord_y}\n')
            
            X.append(coord_x)
            Y.append(coord_y)
            
        output_file.write(f'DEMAND_SECTION\n')
        output_file.write('1 0\n')
        
        for i in range(2,num_nodes+1):
            output_file.write(f'{i} {node_demand[i]}\n')
        
        output_file.write(f'DEPOT_SECTION\n')
        output_file.write('1\n-1\nEOF\n')  

        plt.figure(figsize=(10,10))
        plt.scatter(X, Y, c='blue', marker='.')
        plt.scatter(X[0], Y[0], c='red', marker='o')        
        plt.savefig(f'{file_name}.png', bbox_inches='tight')          
        
        
    def generate_gaussian(self, file_name, instance_name, num_nodes, capacity, seed):
    
        # Initialize random seed
        random.seed(seed)
        
        X = []
        Y = []
            
        # Setting some bounds about capacity to generate only feasible solutions
        total_demand = 0
        node_demand = dict()
        for i in range(1,num_nodes+1):
            demand = random.randint(1, capacity)
            node_demand[i] = demand
            total_demand += demand
            
        print(f'Total demand: {total_demand}\n')
            
        # Estimate the number of vehicles needed to solve the problem
        num_vehicles = math.ceil(total_demand / capacity)
    
        # Creates an empty file to write instances from data
        output_file = open(f'{file_name}.vrp', 'w+')
        
        # Writes the file header, considering the input file is described as EUC_2D CVRP format
        output_file.write(f'NAME : {instance_name}\n') 
        output_file.write(f'COMMENT : Random generated instance, No. of vehicles {num_vehicles}, capacity {capacity}, Optimal value: Unknown\n') 
        output_file.write(f'TYPE : CVRP\n') 
        output_file.write(f'DIMENSION : {num_nodes}\n') 
        output_file.write(f'EDGE_WEIGHT_TYPE : EUC_2D\n') 
        output_file.write(f'CAPACITY : {capacity}\n')
        output_file.write(f'NODE_COORD_SECTION\n')
        
        coord_x0 = random.uniform(0.0, 1.0)
        coord_y0 = random.uniform(0.0, 1.0)
        output_file.write(f'1 {coord_x0} {coord_y0}\n')

        X.append(coord_x0)
        Y.append(coord_y0)
        
        for i in range(2,num_nodes+1):
        
            while(True):
                coord_x = random.gauss(coord_x0, 1.0)
                if coord_x > 0.0 and coord_x < 1.0:
                    break
            while(True):
                coord_y = random.uniform(coord_y0, 1.0)
                if coord_y > 0.0 and coord_y < 1.0:
                    break
        
            output_file.write(f'{i} {coord_x} {coord_y}\n')
            
            X.append(coord_x)
            Y.append(coord_y)
            
        output_file.write(f'DEMAND_SECTION\n')
        output_file.write('1 0\n')
        
        for i in range(2,num_nodes+1):
            output_file.write(f'{i} {node_demand[i]}\n')
        
        output_file.write(f'DEPOT_SECTION\n')
        output_file.write('1\n-1\nEOF\n')  

        plt.figure(figsize=(10,10))
        plt.scatter(X, Y, c='blue', marker='.')
        plt.scatter(X[0], Y[0], c='red', marker='o')        
        plt.savefig(f'{file_name}.png', bbox_inches='tight')        
  
# Read command-line arguments to inform generator  
def main():

    # Check if all parameters were informed
    if len(sys.argv) != 6:
        print('\n\nError: invalid syntax.\nUsage: python cvrp-rand-gen.py <seed> <instance-name> <instance-file> <nodes> <capacity>\n\n')
        return

    # Gets the parameters from command line
    r_seed = int(sys.argv[1])
    instance = sys.argv[2]
    output_file = sys.argv[3]
    nodes = int(sys.argv[4])
    capacity = int(sys.argv[5])   
    
    print('\nCVRP Random Seed\n')
    print(f'Seed    : {r_seed}')
    print(f'Name    : {instance}')
    print(f'File    : {output_file}')
    print(f'# Nodes : {nodes}')
    print(f'Capacity: {capacity}\n\n')
    
    # Runs the generator
    gen = RndGenCVRP()
    gen.generate_uniform(output_file, instance, nodes, capacity, r_seed)  
    #gen.generate_gaussian(output_file, instance, nodes, capacity, r_seed)
   
# Call the main function   
main()