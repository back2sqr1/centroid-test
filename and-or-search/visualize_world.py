import json
import matplotlib.pyplot as plt
import numpy as np

def visualize_world():
    # Load data
    try:
        with open('generated_bdd.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: generated_bdd.json not found.")
        return

    # Create figure with two subplots
    fig = plt.figure(figsize=(16, 8))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1])
    
    ax_map = fig.add_subplot(gs[0])
    ax_bdd = fig.add_subplot(gs[1])

    # --- Plot 1: 2D Coordinate Grid (Map) ---
    locations = data['locations']
    prop_to_loc = data['prop_to_location']
    
    # Invert prop_to_loc to get loc_to_props
    loc_to_props = {loc: [] for loc in locations}
    for prop, locs in prop_to_loc.items():
        for loc in locs:
            if loc in loc_to_props:
                loc_to_props[loc].append(prop)
    
    # Extract coordinates
    x_coords = []
    y_coords = []
    names = []
    
    for name, coords in locations.items():
        names.append(name)
        x_coords.append(coords[0])
        y_coords.append(coords[1])
        
        # Annotate
        props_str = ", ".join(sorted(loc_to_props[name]))
        label = f"{name}\n[{props_str}]"
        ax_map.text(coords[0], coords[1] + 0.5, label, ha='center', va='bottom', fontsize=9, bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    # Scatter plot
    ax_map.scatter(x_coords, y_coords, c='blue', s=100, zorder=5)
    
    # Set grid and labels
    ax_map.grid(True, linestyle='--', alpha=0.6)
    ax_map.set_title("World Map (Locations & Properties)")
    ax_map.set_xlabel("X Coordinate")
    ax_map.set_ylabel("Y Coordinate")
    ax_map.axis('equal')
    
    # Add some padding to limits
    if x_coords and y_coords:
        x_range = max(x_coords) - min(x_coords)
        y_range = max(y_coords) - min(y_coords)
        margin = max(x_range, y_range) * 0.2 if max(x_range, y_range) > 0 else 5
        ax_map.set_xlim(min(x_coords) - margin, max(x_coords) + margin)
        ax_map.set_ylim(min(y_coords) - margin, max(y_coords) + margin)

    # --- Plot 2: BDD Structure ---
    import graphviz
    print("Attempting to render BDD with Graphviz...")
    
    dot = graphviz.Digraph(comment='BDD', format='png')
    dot.attr(rankdir='TB')
    
    nodes = data['nodes']
    
    # Add nodes
    for node_id, node_data in nodes.items():
        if node_id in ['true', 'false']:
            dot.node(node_id, node_id, shape='box', color='green' if node_id == 'true' else 'red', style='filled', fillcolor='lightgreen' if node_id == 'true' else 'lightpink')
        else:
            var = node_data.get('var', '?')
            dot.node(node_id, f"{node_id}\n({var})", shape='circle', style='filled', fillcolor='lightblue')
            
            # Edges
            low = node_data.get('low')
            high = node_data.get('high')
            if low:
                dot.edge(node_id, low, style='dashed', label='0')
            if high:
                dot.edge(node_id, high, style='solid', label='1')
    
    # Render to file
    # This will create bdd_viz.png
    output_path = dot.render('bdd_viz', view=False)
    print(f"Graphviz rendered to {output_path}")
    
    # Display in matplotlib
    img = plt.imread(output_path)
    ax_bdd.imshow(img)
    ax_bdd.axis('off')
    ax_bdd.set_title("BDD Logic Structure (Graphviz)")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    visualize_world()
