# ds_wordsim
A simple word similarity/antonym detector based on a manually created word network


Main interface to the code:

1) To read the data file and create the network: parse_dictionary(file_name). This returns a python dict [node_map]
2) To check for connection: find_connection(word1, word2, node_map). Returns an enum type
    SIMILAR = 0
    OPPOSITE = 1
    NONE = 2

If debug mode is set to true, this method will also print out the path between the two nodes.

Check the example file main_word_similarity.py for usage
