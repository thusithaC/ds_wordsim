'''
Parse the dictionary text and create a network of Nodes
'''

from enum import Enum
import re


class Relation(Enum):
    SIMILAR = 0
    OPPOSITE = 1
    NONE = 2

class Edge():
    def __init__(self, nodeL, nodeR, type):
        self.node_left = nodeL
        self.node_right = nodeR
        self.type = type
    def reverse(self):
        return Edge(self.node_right, self.node_left, self.type)

    def __repr__(self):
        rep = "From " + self.node_left.text + " to " + self.node_right.text + " - " + str(self.type)
        return rep


class Node():
    def __init__(self, word):
        self.text = word
        self.edges = []

    def add_neighbor_as_edge(self, edge):
        # always left node is to yourself
        if not isinstance(edge, Edge):
            raise TypeError("Should pass in a type of Edge")
        self.edges.append(edge)

    def get_neighbors(self):
        return self.edges

    def __repr__(self):
        rep = "\nKey:[" + self.text + "] with edges:\n"
        edges_str = '\t' + '\n\t'.join([str(x) for x in self.edges])
        rep = rep + edges_str + "\n\n"
        return rep


EVENT_START_OR_END = '='
EVENT_KEY_LINE = 'KEY:'
EVENT_SYN_LINE = 'SYN:'
EVENT_ANT_LINE = 'ANT:'
STATE_P = "PROCESSING"
STATE_PK = "PROCESSING_FOUND_KEY"
STATE_PS = "PROCESSING_SYN"
STATE_PA = "PROCESSING_ANT"
STATE_W = "WAITING_FOR_NEW"

def parse_dictionary(data_dictionary_path):

    node_map = dict()
    with open(data_dictionary_path) as dfile:
        state = STATE_W
        current_key = ''
        key_node = None
        for line in dfile:
            if line == '' or line =='.' or line == ',' or line == '\n':
                continue
            if line[0] == EVENT_START_OR_END:
                state = STATE_P
                print('\n')
                continue

            if line[0:4] == EVENT_KEY_LINE and state == STATE_P:
                pat = re.compile('.*\[See .*\].*')
                pat_alpha = re.compile('^[a-z\-]+$')
                line = line.strip('\n')
                line = line.replace('\\n', ' ').replace('\\a', ' ').replace('\\r', ' ').replace('\\v', ' ')
                line = line.replace('_', '-')
                if re.match(pat, line):
                    # first check if there are other keys than the [See X] one
                    split_by_brack = line.split(': ')[1].split('[')
                    if split_by_brack[0] == '':
                        split_by_brack.pop(0)
                    if split_by_brack[0].find(']') > 0: #first token is the [See X] type
                        split_by_brack[0] = split_by_brack[0].strip(' ').replace('.', '').replace(',', '') #TODO: more work to be done here
                        limit = split_by_brack[0].find(']')
                        key = split_by_brack[0][4:limit].lower().strip('-')
                        if re.match(pat_alpha, key):
                            current_key = key
                        else:
                            current_key = ''
                            print("Cant find suitable key " + line)
                    else: # first token is a normal type
                        split_by_space = split_by_brack[0].lower().split(' ')
                        key = split_by_space[0].lower().replace('.', '').replace(',', '').strip('-')
                        if re.match(pat_alpha, key):
                            current_key = key
                        else:
                            current_key = ''
                            print("Cant find suitable key " + line)
                else:
                    split_by_col = line.split(': ')
                    if len(split_by_col) > 1:
                        key = split_by_col[1].split(' ')[0].lower().replace('.', '').replace(',', '').strip('-')
                        if re.match(pat_alpha, key):
                            current_key = key
                        else:
                            current_key = ''
                            print("Cant find suitable key " + line)
                    else:
                        current_key = ''
                        print("Cant find suitable key " + line)
                if current_key != '':
                    print("Picked up key " + current_key)

                    if node_map.get(current_key) is None:
                        key_node = Node(current_key)
                        node_map[current_key] = key_node
                    else:
                        key_node = node_map.get(current_key)
                state = STATE_PK
                continue

            if line[0:4] == EVENT_SYN_LINE and state == STATE_PK:
                if current_key == '':
                    continue
                state = STATE_PS
                syn_line = line[4:].replace('\n', '')
                words = parse_line(syn_line)
                print(state + " " + ' '.join(words))
                create_nodes(words, key_node, Relation.SIMILAR, node_map)
                # process syn line
                continue

            if line[0:4] == EVENT_ANT_LINE and (state == STATE_PS or state == STATE_PK):
                if current_key == '':
                    continue
                state = STATE_PA
                ant_line = line[4:].replace('\n', '')
                words = parse_line(ant_line)
                print(state + " " + ' '.join(words))
                create_nodes(words, key_node, Relation.OPPOSITE, node_map)
                continue

            if state == STATE_PS: #new line with synonyms
                if current_key == '':
                    continue
                syn_line = line.replace('\n', '')
                words = parse_line(syn_line)
                print(state + " " + ' '.join(words))
                create_nodes(words, key_node, Relation.SIMILAR, node_map)
                continue
            if state == STATE_PA: #new line with antonyms
                if current_key == '':
                    continue
                ant_line = line.replace('\n', '')
                words = parse_line(ant_line)
                print(state + " " + ' '.join(words))
                create_nodes(words, key_node, Relation.SIMILAR, node_map)
                continue

            # tying to catch errors:
            if line[0:4] == EVENT_SYN_LINE and state != STATE_P:
                raise RuntimeError("line improperly formatted" + line)
            if line[0:4] == EVENT_ANT_LINE and not (state == STATE_PS or state == STATE_P):
                raise RuntimeError("line improperly formatted" + line)
            if state != STATE_PK:
                raise RuntimeError("No suitable extraction found. line improperly formatted " + line)
            # end of line processing
    return node_map


def parse_line(line:str):
    pat_alpha = re.compile('^[a-z\-]+$')
    line = line.replace('.', '').replace(',', '').strip(' ').strip('\n')
    line = line.lower()
    words = [w for w in line.split() if (w != '' and pat_alpha.match(w))]
    return words

def create_nodes(words:list, key_node:Node, relation:Relation, map:dict):
    for word in words:
        if map.get(word) is None:
            node = Node(word)
            map[word] = node
        else:
            node = map.get(word)
        edge_key = Edge(key_node, node, relation)  # always left node is to yourself
        key_node.add_neighbor_as_edge(edge_key)
        node.add_neighbor_as_edge(edge_key.reverse())


def bfs(root:Node, dest:Node):
    ''' Does BFS and returns a list of edges'''
    from queue import Queue

    if root is None or len(root.edges) == 0 or dest is None or len(dest.edges) == 0:
        return []
    if root.text == dest.text:
        return [Edge(root, root, Relation.SIMILAR)]
    processed = set()
    pq = Queue()
    path_list = []
    pq.put((root, []))
    processed.add(root.text)
    while not pq.empty():
        found = False
        processing_node, path = pq.get()
        children = [(x.node_right, x) for x in processing_node.edges if x.node_right.text not in processed]
        for n, e in children:
            path_to_child = [p for p in path]
            path_to_child.append(e)
            pq.put((n, path_to_child))
            processed.add(n.text)
            if n.text == dest.text:
                found = True
                path_list = path_to_child
                break
        if found:
            break
    # outside while
    return path_list

def __find_connection__(word1:str, word2:str, node_map:dict, cutoff=3, debug=False):
    if debug:
        print("Words: " + word1 + " and " + word2)
    node_1 = node_map.get(word1)
    node_2 = node_map.get(word2)

    if node_1 is None or node_2 is None:
        return Relation.NONE
    edge_list = bfs(node_1, node_2)
    if debug:
        print("\n".join([str(x) for x in edge_list]))

    if len(edge_list) == 0 or len(edge_list) > cutoff:
        return Relation.NONE
    opposite_edges = [x for x in edge_list if x.type == Relation.OPPOSITE]
    if debug:
        print("Opposite edges:  " + "\n".join([str(x) for x in opposite_edges]))
    if len(opposite_edges) % 2 == 0:
        return Relation.SIMILAR
    else:
        return Relation.OPPOSITE

def find_connection(word1:str, word2:str, node_map:dict, cutoff=3, debug=False):
    connection_left = __find_connection__(word1, word2, node_map, cutoff, debug)
    connection_right = __find_connection__(word2, word1, node_map, cutoff, debug)

    if debug:
        print("Found connection {} from L->R and connection {} from R->L".format(connection_left, connection_right))
    if connection_left == Relation.SIMILAR and connection_right == Relation.OPPOSITE:
        print("Warning Mismatching left and right Relationships for {} nd {}".format(word1, word2))
        return Relation.NONE
    elif connection_left == Relation.OPPOSITE and connection_right == Relation.SIMILAR:
        print("Warning Mismatching left and right Relationships for {} nd {}".format(word1, word2))
        return Relation.NONE
    elif connection_left == Relation.NONE:
        return connection_right
    else:
        return connection_left



