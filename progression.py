# progression.py
# Calvin Pelletier
# 12/26/15

import csv
from random import randint

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
    for i in range(max_chords + 1):
        for node in temp:
            for chord in viable_chords:
                newNode = TreeNode(chord)
                queue.append(newNode)
                if i == max_chords:
                    node.children.append(TreeConnection(0, newNode))
                else:
                    node.children.append(TreeConnection(default_weight, newNode))
            if i >= min_chords:
                node.children.append(TreeConnection(default_weight, TreeNode('END')))
            else:
                node.children.append(TreeConnection(0, TreeNode('END')))
        temp = queue
        queue = []
    return root

def print_tree(node, depth):
    if len(node.children) == 0:
        return
    print("(%d:%s " % (depth, node.data)),
    for connection in node.children:
        print("%d-%s" % (connection.weight, connection.to_node.data)),
    print(")")
    for connection in node.children:
        print_tree(connection.to_node, depth + 1)

def teach_decision_tree(file, root):
    csvfile = open(file, 'rb')
    reader = csv.reader(csvfile, delimiter='\t')
    for line in reader:
        temp = root
        for chord in range(len(line) - 1):
            for connection in temp.children:
                if connection.to_node.data == line[chord]:
                    connection.weight += int(line[len(line) - 1])
                    temp = connection.to_node
                    break
        for connection in temp.children:
            if connection.to_node.data == 'END':
                connection.weight += int(line[len(line) - 1])
    csvfile.close()

def create_progression(root, double_progession_chance):
    temp = root
    ret = []
    while 1:
        # base case
        if temp.data == 'END':
            break;
        # find random number
        total = 0
        for connection in temp.children:
            total += connection.weight
        if total == 1:
            rand = 0
        else:
            rand = randint(0, total - 1)
        # choose chord based on random number
        total = 0
        for connection in temp.children:
            total += connection.weight
            if rand < total:
                temp = connection.to_node
                if temp.data != 'END':
                    ret.append(temp.data)
                break
    #append a second progression if desired (common in many songs to have an 8-chord progression built from two 4 chord progressions)
    if (randint(0,100) / 100.0) < double_progession_chance:
        ret2 = []
        temp = root
        while 1:
            # base case
            if temp.data == 'END':
                break;
            # find random number
            total = 0
            for connection in temp.children:
                total += connection.weight
            if total == 1:
                rand = 0
            else:
                rand = randint(0, total - 1)
            # choose chord based on random number
            total = 0
            for connection in temp.children:
                total += connection.weight
                if rand < total:
                    temp = connection.to_node
                    if temp.data != 'END':
                        ret.append(temp.data)
                    break
        ret += ret2
    return ret

def print_n_progressions(root, n):
    dict = {}
    for i in range(n):
        progression = '-'.join(create_progression(root))
        if dict.has_key(progression):
            dict[progression] += 1
        else:
            dict[progression] = 1
    for key in dict:
        print("%d\t%s" % (dict[key], key))

def std_initialization():
    root = build_decision_tree(2, 6, 1, ['I', 'ii', 'iii', 'III', 'IV', 'V', 'vi'])
    teach_decision_tree("progression_data.txt", root)
    return root

def note_in_chord(note, chord):
    if chord == 'I':
        if note == 1 or note == 3 or note == 5:
            return True
    elif chord == 'ii':
        if note == 2 or note == 4 or note == 5:
            return True
    elif chord == 'iii':
        if note == 3 or note == 5 or note == 7:
            return True
    elif chord == 'III':
        if note == 3 or note == 7:
            return True
    elif chord == 'IV':
        if note == 4 or note == 6 or note == 1:
            return True
    elif chord == 'V':
        if note == 5 or note == 7 or note == 2:
            return True
    elif chord == 'vi':
        if note == 6 or note == 1 or note == 3:
            return True
    return False
