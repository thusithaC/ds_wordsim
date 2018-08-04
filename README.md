# ds_wordsim
A simple word similarity/antonym detector based on a manually created word network
Check the example file main_word_similarity.py for usage

The question I tried to address through this project is given two words, are they synonyms or antonyms or not directly related at all

Main interface to the code:

1) To read the data file and create the network:
```python
parse_dictionary(file_name). 
```
This returns a python dict [node_map]
2) To check for connection: 
```python
find_connection(word1, word2, node_map). Returns an enum type
    SIMILAR = 0
    OPPOSITE = 1
    NONE = 2
```

If debug mode is set to true, this method will also print out the path between the two nodes.

```python
print(find_connection("sweet", "hot", node_map, 5, debug=True))
Words: sweet and hot
From sweet to acrid - Relation.OPPOSITE
From acrid to pungent - Relation.SIMILAR
From pungent to hot - Relation.SIMILAR
Opposite edges:  From sweet to acrid - Relation.OPPOSITE
Words: hot and sweet
From hot to pungent - Relation.SIMILAR
From pungent to acrimonious - Relation.SIMILAR
From acrimonious to sweet - Relation.OPPOSITE
Opposite edges:  From acrimonious to sweet - Relation.OPPOSITE
Found connection Relation.OPPOSITE from L->R and connection Relation.OPPOSITE from R->L
Relation.OPPOSITE
```


