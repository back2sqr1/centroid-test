import matplotlib.pyplot as plt
import numpy as np

def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def run_simulation(ax, sim_index):
    # Grid settings
    grid_size = 100
    
    # Initial Robot Positions (Set to None to randomize)
    Start1 = None
    Start2 = None
    
    if Start1 is None:
        Start1 = np.random.rand(2) * grid_size
    if Start2 is None:
        Start2 = np.random.rand(2) * grid_size
    
    A = np.random.rand(2) * grid_size
    B = np.random.rand(2) * grid_size
    C = np.random.rand(2) * grid_size
    
    # Calculate max travel distance allowed for Robot 2
    max_travel_dist = distance(Start1, A)
    
    # Generate random D values within valid range
    num_samples = 1000  # Increased samples
    Ds = []
    while len(Ds) < num_samples:
        angle = np.random.uniform(0, 2 * np.pi)
        r = np.sqrt(np.random.uniform(0, 1)) * max_travel_dist
        
        dx = r * np.cos(angle)
        dy = r * np.sin(angle)
        candidate = Start2 + np.array([dx, dy])
        Ds.append(candidate)
            
    Ds = np.array(Ds)
    
    results_B = []
    results_C = []
    
    for i, D in enumerate(Ds):
        R1_pos = A
        R2_pos = D
        
        dist_to_B_from_R1 = distance(R1_pos, B)
        dist_to_B_from_R2 = distance(R2_pos, B)
        min_dist_B = min(dist_to_B_from_R1, dist_to_B_from_R2)
        
        dist_to_C_from_R1 = distance(R1_pos, C)
        dist_to_C_from_R2 = distance(R2_pos, C)
        min_dist_C = min(dist_to_C_from_R1, dist_to_C_from_R2)
        
        results_B.append(min_dist_B)
        results_C.append(min_dist_C)

    # Visualization on ax
    ax.axis('equal')
    
    # Plot Start Positions
    ax.scatter(Start1[0], Start1[1], c='pink', s=100, label='Start 1', marker='s', edgecolors='black', zorder=9)
    ax.scatter(Start2[0], Start2[1], c='lightblue', s=100, label='Start 2', marker='s', edgecolors='black', zorder=9)
    ax.text(Start1[0]+2, Start1[1]+2, 'Start1', fontsize=8, fontweight='bold')
    ax.text(Start2[0]+2, Start2[1]+2, 'Start2', fontsize=8, fontweight='bold')

    # Plot A, B, C
    ax.scatter(A[0], A[1], c='red', s=150, label='A (R1 Final)', marker='^', edgecolors='black', zorder=10)
    ax.scatter(B[0], B[1], c='green', s=150, label='B (Target)', marker='*', edgecolors='black', zorder=10)
    ax.scatter(C[0], C[1], c='blue', s=150, label='C (Target)', marker='*', edgecolors='black', zorder=10)
    
    # Draw movement of Robot 1
    ax.arrow(Start1[0], Start1[1], A[0]-Start1[0], A[1]-Start1[1], head_width=2, color='pink', length_includes_head=True, alpha=0.6)

    # Draw reachable area for Robot 2
    circle = plt.Circle((Start2[0], Start2[1]), max_travel_dist, color='lightblue', alpha=0.1)
    ax.add_patch(circle)
    theta = np.linspace(0, 2*np.pi, 100)
    cx = Start2[0] + max_travel_dist * np.cos(theta)
    cy = Start2[1] + max_travel_dist * np.sin(theta)
    ax.plot(cx, cy, 'b--', alpha=0.3)

    # Plot Ds
    # Metric: Minimize the Maximum of the two distances (Minimax)
    results_B_arr = np.array(results_B)
    results_C_arr = np.array(results_C)
    optimization_metric = np.maximum(results_B_arr, results_C_arr)
    
    sc = ax.scatter(Ds[:, 0], Ds[:, 1], c=optimization_metric, cmap='viridis_r', s=20, alpha=0.6, edgecolors='none')
    
    # Add colorbar for this specific subplot
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label('Max(MinDist(B), MinDist(C))', fontsize=8)
    
    # Annotate A, B, C
    ax.text(A[0]+2, A[1]+2, 'A', fontsize=10, fontweight='bold')
    ax.text(B[0]+2, B[1]+2, 'B', fontsize=10, fontweight='bold')
    ax.text(C[0]+2, C[1]+2, 'C', fontsize=10, fontweight='bold')
    
    # Best D
    # Primary metric: Minimize Max(X, Y)
    # Secondary metric: Minimize Sum(X, Y) (Tie-breaker)
    secondary_metric = results_B_arr + results_C_arr
    
    # Use lexsort to find the index. lexsort sorts by the last key first, then the second to last, etc.
    # We want primary=optimization_metric, secondary=secondary_metric.
    # So we pass (secondary_metric, optimization_metric) to lexsort.
    sorted_indices = np.lexsort((secondary_metric, optimization_metric))
    best_idx = sorted_indices[0]
    
    best_D = Ds[best_idx]
    
    ax.scatter(best_D[0], best_D[1], c='gold', s=200, marker='P', edgecolors='black', zorder=11)
    ax.text(best_D[0]+2, best_D[1]-2, 'Best D', fontsize=8, fontweight='bold')

    # Draw movement of Robot 2 to Best D
    ax.arrow(Start2[0], Start2[1], best_D[0]-Start2[0], best_D[1]-Start2[1], head_width=2, color='lightblue', length_includes_head=True, alpha=0.8)

    # Draw lines from Best D scenario
    if distance(A, B) < distance(best_D, B):
        ax.plot([A[0], B[0]], [A[1], B[1]], 'k--', alpha=0.5)
    else:
        ax.plot([best_D[0], B[0]], [best_D[1], B[1]], 'k--', alpha=0.5)
        
    if distance(A, C) < distance(best_D, C):
        ax.plot([A[0], C[0]], [A[1], C[1]], 'k:', alpha=0.5)
    else:
        ax.plot([best_D[0], C[0]], [best_D[1], C[1]], 'k:', alpha=0.5)

    ax.set_title(f"Sim {sim_index}: Max Dist={max_travel_dist:.1f}\nBest Max-Min Dist={optimization_metric[best_idx]:.1f}", fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    return sc

def main():
    # Create 2x4 subplots
    fig, axes = plt.subplots(2, 4, figsize=(24, 12))
    axes = axes.flatten()
    
    for i, ax in enumerate(axes):
        run_simulation(ax, i+1)
        
    plt.suptitle("Robot Logistics Simulation - 8 Random Scenarios", fontsize=16)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
