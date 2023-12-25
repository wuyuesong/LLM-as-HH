from aco import ACO
import sys
import numpy as np
from scipy.spatial import distance_matrix
import logging

from gpt import heuristics_v2 as heuristics


N_ITERATIONS = 100
N_ANTS = 30
CAPACITY = 50


if __name__ == "__main__":
    print("[*] Running ...")

    problem_size = int(sys.argv[1])
    root_dir = sys.argv[2]
    mood = sys.argv[3]
    assert mood in ['train', 'val']
    
    if mood == 'train':
    
        dataset_path = f"{root_dir}/problems/cvrp_aco/dataset/{mood}{problem_size}_dataset.npy"
        dataset = np.load(dataset_path)
        demands, node_positions = dataset[:, :, 0], dataset[:, :, 1:]
        
        n_instances = node_positions.shape[0]
        print(f"[*] Dataset loaded: {dataset_path} with {n_instances} instances.")
        
        objs = []
        for i, (node_pos, demand) in enumerate(zip(node_positions, demands)):
            dist_mat = distance_matrix(node_pos, node_pos)
            dist_mat[np.diag_indices_from(dist_mat)] = 1 # set diagonal to a large number
            heu = heuristics(dist_mat, node_pos, demand, CAPACITY) + 1e-9
            heu[heu < 1e-9] = 1e-9
            aco = ACO(dist_mat, demand, heu, CAPACITY, n_ants=N_ANTS)
            obj = aco.run(N_ITERATIONS)
            print(f"[*] Instance {i}: {obj}")
            objs.append(obj)
        
        print("[*] Average:")
        print(np.mean(objs))
        
    else:
        for problem_size in [20, 50, 100]:
    
            dataset_path = f"{root_dir}/problems/cvrp_aco/dataset/{mood}{problem_size}_dataset.npy"
            dataset = np.load(dataset_path)
            demands, node_positions = dataset[:, :, 0], dataset[:, :, 1:]
            
            n_instances = node_positions.shape[0]
            logging.info(f"[*] Evaluating {dataset_path}")
            
            objs = []
            for i, (node_pos, demand) in enumerate(zip(node_positions, demands)):
                dist_mat = distance_matrix(node_pos, node_pos)
                dist_mat[np.diag_indices_from(dist_mat)] = 1 # set diagonal to a large number
                heu = heuristics(dist_mat, node_pos, demand, CAPACITY) + 1e-9
                heu[heu < 1e-9] = 1e-9
                aco = ACO(dist_mat, demand, heu, CAPACITY, n_ants=N_ANTS)
                obj = aco.run(N_ITERATIONS)
                objs.append(obj.item())
            
            print(f"[*] Average for {problem_size}: {np.mean(objs)}")