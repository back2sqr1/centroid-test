import matplotlib.pyplot as plt
import numpy as np

def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def solve_step(mover_pos, support_pos, target_pos, next_targets, ax, title, labels):
    # Calculate max travel distance (distance mover travels to target)
    max_travel_dist = distance(mover_pos, target_pos)
    
    # Generate random candidates for support robot
    num_samples = 2000
    candidates = []
    # Always include staying put
    candidates.append(support_pos)
    
    while len(candidates) < num_samples:
        angle = np.random.uniform(0, 2 * np.pi)
        r = np.sqrt(np.random.uniform(0, 1)) * max_travel_dist
        dx = r * np.cos(angle)
        dy = r * np.sin(angle)
        cand = support_pos + np.array([dx, dy])
        candidates.append(cand)
    
    candidates = np.array(candidates)
    
    # Evaluate candidates
    # Metric: Minimize Max(MinDist(NextTarget1), MinDist(NextTarget2))
    scores = []
    for cand in candidates:
        target_scores = []
        for nt in next_targets:
            d1 = distance(target_pos, nt)
            d2 = distance(cand, nt)
            target_scores.append(min(d1, d2))
        
        # Minimax
        scores.append(max(target_scores))
        
    scores = np.array(scores)
    best_idx = np.argmin(scores)
    best_candidate = candidates[best_idx]
    
    # Visualization
    ax.axis('equal')
    
    # Plot Start Positions
    ax.scatter(mover_pos[0], mover_pos[1], c='pink', s=100, marker='s', edgecolors='black', zorder=9)
    ax.text(mover_pos[0]+2, mover_pos[1]+2, labels['mover_start'], fontsize=8)
    
    ax.scatter(support_pos[0], support_pos[1], c='lightblue', s=100, marker='s', edgecolors='black', zorder=9)
    ax.text(support_pos[0]+2, support_pos[1]+2, labels['support_start'], fontsize=8)
    
    # Plot Target
    ax.scatter(target_pos[0], target_pos[1], c='red', s=150, marker='^', edgecolors='black', zorder=10)
    ax.text(target_pos[0]+2, target_pos[1]+2, labels['target'], fontsize=10, fontweight='bold')
    
    # Plot Next Targets
    colors = ['green', 'blue']
    for i, nt in enumerate(next_targets):
        ax.scatter(nt[0], nt[1], c=colors[i % 2], s=150, marker='*', edgecolors='black', zorder=10)
        ax.text(nt[0]+2, nt[1]+2, labels['next'][i], fontsize=10, fontweight='bold')
        
    # Draw Mover Arrow
    ax.arrow(mover_pos[0], mover_pos[1], target_pos[0]-mover_pos[0], target_pos[1]-mover_pos[1], 
             head_width=2, color='pink', length_includes_head=True, alpha=0.6)
             
    # Draw Reachable Area
    circle = plt.Circle((support_pos[0], support_pos[1]), max_travel_dist, color='lightblue', alpha=0.1)
    ax.add_patch(circle)
    theta = np.linspace(0, 2*np.pi, 100)
    cx = support_pos[0] + max_travel_dist * np.cos(theta)
    cy = support_pos[1] + max_travel_dist * np.sin(theta)
    ax.plot(cx, cy, 'b--', alpha=0.3)
    
    # Plot Heatmap
    sc = ax.scatter(candidates[:, 0], candidates[:, 1], c=scores, cmap='viridis_r', s=20, alpha=0.6, edgecolors='none')
    plt.colorbar(sc, ax=ax, label='Max MinDist to Next Targets')
    
    # Plot Best Candidate
    ax.scatter(best_candidate[0], best_candidate[1], c='gold', s=200, marker='P', edgecolors='black', zorder=11)
    ax.text(best_candidate[0]+2, best_candidate[1]-2, labels['best'], fontsize=9, fontweight='bold')
    
    # Draw Support Arrow
    ax.arrow(support_pos[0], support_pos[1], best_candidate[0]-support_pos[0], best_candidate[1]-support_pos[1],
             head_width=2, color='lightblue', length_includes_head=True, alpha=0.8)
             
    ax.set_title(title)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    return best_candidate

def main():
    grid_size = 100
    # Define locations
    locs = {}
    for name in ['Start1', 'Start2', 'A', 'B', 'C', 'E', 'F', 'G', 'H']:
        locs[name] = np.random.rand(2) * grid_size
        
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    
    # Step 1: Go to A. Find D.
    # Robot 1 (Start1) goes to A. Robot 2 (Start2) goes to D.
    # Next targets: B, C.
    ax1 = axes[0]
    D = solve_step(
        mover_pos=locs['Start1'],
        support_pos=locs['Start2'],
        target_pos=locs['A'],
        next_targets=[locs['B'], locs['C']],
        ax=ax1,
        title="Step 1: To A, Find D",
        labels={'mover_start': 'Start1', 'support_start': 'Start2', 'target': 'A', 'next': ['B', 'C'], 'best': 'D'}
    )
    
    # Current State: R1 at A, R2 at D.
    
    # Step 2B: B Universe. Go to B. Find I.
    # Next targets: E, F.
    # Who goes to B? Closer of A or D.
    dist_A_B = distance(locs['A'], locs['B'])
    dist_D_B = distance(D, locs['B'])
    
    if dist_A_B < dist_D_B:
        mover_pos = locs['A']
        mover_name = 'R1(A)'
        support_pos = D
        support_name = 'R2(D)'
    else:
        mover_pos = D
        mover_name = 'R2(D)'
        support_pos = locs['A']
        support_name = 'R1(A)'
        
    ax2 = axes[1]
    I = solve_step(
        mover_pos=mover_pos,
        support_pos=support_pos,
        target_pos=locs['B'],
        next_targets=[locs['E'], locs['F']],
        ax=ax2,
        title="Step 2 (B Universe): To B, Find I",
        labels={'mover_start': mover_name, 'support_start': support_name, 'target': 'B', 'next': ['E', 'F'], 'best': 'I'}
    )
    
    # Step 2C: C Universe. Go to C. Find J.
    # Next targets: G, H.
    # Who goes to C? Closer of A or D.
    dist_A_C = distance(locs['A'], locs['C'])
    dist_D_C = distance(D, locs['C'])
    
    if dist_A_C < dist_D_C:
        mover_pos = locs['A']
        mover_name = 'R1(A)'
        support_pos = D
        support_name = 'R2(D)'
    else:
        mover_pos = D
        mover_name = 'R2(D)'
        support_pos = locs['A']
        support_name = 'R1(A)'
        
    ax3 = axes[2]
    J = solve_step(
        mover_pos=mover_pos,
        support_pos=support_pos,
        target_pos=locs['C'],
        next_targets=[locs['G'], locs['H']],
        ax=ax3,
        title="Step 2 (C Universe): To C, Find J",
        labels={'mover_start': mover_name, 'support_start': support_name, 'target': 'C', 'next': ['G', 'H'], 'best': 'J'}
    )
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()

"""
Consider this problem that is attempted to be reflected in interactive_circles.py: 

2 robots need to go to locations (A, B, C, D, ,E, F, G, H). 
The robots first need to go to A. Whenever a robot reaches a location, 
they are then assigned to go to another locations. 
While the first robot (the robot you choose to go to A), the second robot can
go anywhere within the distance that the first robot traveled to reach A, and 
try to minimize the amount of distance to the next locations (B, C) after A. 
Call this location that minimizes the distance to B and C within the distance of the 
first robot traveled as D.

Then with the new positions of the robots (first robot at A, second robot at D), 
show two graphs with one of the robots going to B (call it the B universe, and the robot
the new first robot), and the other with one of the robots going to C (call it the C universe, and the robot
the new first robot)

In the B universe, the other robot (not the new first robot going to B) 
going to anywhere within the distance of the new first robot traveled to B 
to minimize the distance to the next locations (E, F). Call this new location I.

In the C universe, the other robot (not the new first robot going to C)
going to anywhere within the distance of the new first robot traveled to C
to minimize the distance to the next locations (G, H). Call this new location J.

Output graphs for all of these steps, showing the positions of the robots, the reachable areas,
and the optimal locations (D, I, J) chosen to minimize the distances to the next locations.

Use the code structure in interactive_circles.py to implement this logic. Keep it the same
and sample optimal locations for D, I and J using random sampling within the reachable areas.
"""