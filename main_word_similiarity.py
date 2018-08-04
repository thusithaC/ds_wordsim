from wordsim.word_network import parse_dictionary, find_connection
import pickle
import sys
sys.setrecursionlimit(100000)


DICTIONARY = 'data/synonyms_list_raw.txt'
'''
This is based on the book - Title: A Complete Dictionary of Synonyms and Antonyms
Downloadable at http://www.gutenberg.org/ebooks/51155.mobile
This version I used has been cleaned up a bit to remove any parsing errors. 
'''

if __name__ == '__main__':

    if 1:
        node_map = parse_dictionary(DICTIONARY)
        pickle.dump(node_map, open('data/wordmap.pickle', 'wb'))
    if 1:
        node_map = pickle.load(open('data/wordmap.pickle', 'rb'))

    print(node_map)
    print(find_connection("pride", "regret", node_map, 5))
    print(find_connection("primitive", "modern", node_map))
    print(find_connection("minor", "major", node_map))
    print(find_connection("sweet", "hot", node_map))
    print(find_connection("sweet", "spicy", node_map, 5, debug=True))
    print(find_connection("fancy", "rich", node_map, debug=True))
    print(find_connection("hot", "cool", node_map, debug=True))
    print(find_connection("strong", "cool", node_map, 2, debug=True))
    print(find_connection("cheap", "fancy", node_map, 2, debug=True))