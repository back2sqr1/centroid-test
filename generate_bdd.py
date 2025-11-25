import random

class BDD:
    def __init__(self, ordering):
        self.ordering = ordering
        self.unique = {}
        self.nodes = {}
        self.next_id = 2
        
        # Create constants
        self.nodes[0] = ("CONST", None, None)
        self.nodes[1] = ("CONST", None, None)

    def mk(self, var, low, high):
        if low == high:
            return low
        
        key = (var, low, high)
        if key in self.unique:
            return self.unique[key]
        
        node_id = self.next_id
        self.next_id += 1
        
        self.unique[key] = node_id
        self.nodes[node_id] = (var, low, high)
        return node_id

    def random_bdd(self):
        """Build a random BDD via random Shannon expansion."""
        def build(vars_left):
            if not vars_left:
                return random.choice([0, 1])   # random terminal
            
            v = vars_left[0]
            
            low  = build(vars_left[1:])
            high = build(vars_left[1:])
            
            return self.mk(v, low, high)
        
        root = build(self.ordering)
        return root


def generate_n_bdds(n, ordering):
    """Generate n random BDDs using the same variable ordering."""
    bdds = []
    for _ in range(n):
        bdd = BDD(ordering)
        root = bdd.random_bdd()
        bdds.append((root, bdd))
    return bdds


# ---------- Example usage ----------
if __name__ == "__main__":
    ordering = ["x1", "x2", "x3"]   # choose any order
    n = 5                           # how many BDDs to generate

    results = generate_n_bdds(n, ordering)

    for i, (root, bdd) in enumerate(results):
        print(f"\nBDD #{i+1}, root = {root}")
        for nid, node in bdd.nodes.items():
            print("  ", nid, node)
