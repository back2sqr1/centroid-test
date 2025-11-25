import random
import string
import json

def random_bdd(num_vars=3):
    """Generate a random BDD with variable nodes and locations."""

    # Base BDD structure
    bdd = {
        "nodes": {
            "true": {"value": True},
            "false": {"value": False}
        }
    }

    # Create variable decision nodes
    for i in range(1, num_vars + 1):
        node_id = f"n{i}"
        var = f"x{i}"

        # Low/high edges may go to terminals or later nodes
        low = random.choice(["true", "false", *(f"n{j}" for j in range(i + 1, num_vars + 1))])
        high = random.choice(["true", "false", *(f"n{j}" for j in range(i + 1, num_vars + 1))])

        bdd["nodes"][node_id] = {
            "var": var,
            "low": low,
            "high": high
        }

    # BDD entry point
    bdd["root"] = "n1"

    # Generate random letter-coded locations
    num_locations = random.randint(3, 8)
    letters = list(string.ascii_lowercase[:num_locations])

    # Map letter → random 2D coordinate
    locations = {}
    for letter in letters:
        x = random.randint(0, 20)
        y = random.randint(0, 20)
        locations[letter] = [x, y]

    bdd["locations"] = locations

    # Map each variable to a random subset of letters
    prop_to_location = {}
    for i in range(1, num_vars + 1):
        var = f"x{i}"
        k = random.randint(1, len(letters))
        chosen_letters = random.sample(letters, k)
        prop_to_location[var] = chosen_letters

    bdd["prop_to_location"] = prop_to_location

    # Prune unreachable nodes
    reachable = set()
    queue = [bdd["root"]]
    
    while queue:
        node_id = queue.pop(0)
        if node_id in reachable:
            continue
        reachable.add(node_id)
        
        if node_id in ["true", "false"]:
            continue
            
        node = bdd["nodes"][node_id]
        queue.append(node["low"])
        queue.append(node["high"])
        
    # Filter nodes
    new_nodes = {}
    for node_id in reachable:
        new_nodes[node_id] = bdd["nodes"][node_id]
        
    bdd["nodes"] = new_nodes

    return bdd


def generate_bdds(n, num_vars=3):
    return [random_bdd(num_vars) for _ in range(n)]


if __name__ == "__main__":
    # Generate a single BDD and save it
    bdd = random_bdd(num_vars=4)
    
    # Print to stdout
    print(json.dumps(bdd, indent=4))
    
    # Save to file
    with open('generated_bdd.json', 'w') as f:
        json.dump(bdd, f, indent=4)
