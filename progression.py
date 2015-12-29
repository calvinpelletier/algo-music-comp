# progression.py
# Calvin Pelletier
# 12/26/15

class TreeNode:
    def __init__(self, data):
        self.children = []
        self.data = data

class TreeConnection:
    def __init__(self, weight, to_node):
        self.weight = weight
        self.to_node = to_node

def build_decision_tree(min_chords, max_chords, default_weight, viable_chords):
    root = TreeNode('START')
    temp = [root]
    queue = []
    for i in range(max_chords):
        for node in temp:
            for chord in viable_chords:
                newNode = TreeNode(chord)
                queue.append(newNode)
                node.children.append(TreeConnection(default_weight, newNode))
            if i >= min_chords:
                node.children.append(TreeConnection(default_weight, TreeNode('END')))
            else:
                node.children.append(TreeConnection(0, TreeNode('END')))
        temp = queue
        queue = []
    return root

def print_tree(node, depth):
    print("(%d:%s " % (depth, node.data)),
    for connection in node.children:
        print("%d-%s" % (connection.weight, connection.to_node.data)),
    print(")")
    for connection in node.children:
        print_tree(connection.to_node, depth + 1)

root = build_decision_tree(2, 6, 1, ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'viio'])
print_tree(root, 0)
